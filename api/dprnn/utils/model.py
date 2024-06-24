import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_packed_sequence, pack_sequence, pad_sequence


class DPCL(nn.Module):
    '''
        Implement of Deep Clustering
    '''

    def __init__(self, num_layer=2, nfft=129, hidden_cells=600, emb_D=40, dropout=0.0, bidirectional=True, activation="Tanh"):
        super(DPCL, self).__init__()
        self.emb_D = emb_D
        self.blstm = nn.LSTM(input_size=nfft, hidden_size=hidden_cells, num_layers=num_layer, batch_first=True,
                             dropout=dropout, bidirectional=bidirectional)
        self.dropout = nn.Dropout(dropout)
        self.activation = getattr(torch.nn, activation)()
        self.linear = nn.Linear(
            2*hidden_cells if bidirectional else hidden_cells, nfft * emb_D)
        self.D = emb_D

    def forward(self, x, is_train=True):
        '''
           input: 
                  for train: B x T x F
                  for test: T x F
           return: 
                  for train: B x TF x D
                  for test: TF x D
        '''
        # print("x.data.size() before not is_train ", x.data.size())
        if not is_train:
            x = torch.unsqueeze(x, 0)
            # print("not is_train triggered ", x.data.size())
        # B x T x F -> B x T x hidden
        # print("x.data.size() before self.blstm ", x.data.size())
        # print("x.data.size()", x.data.size()) # errors\
        x, _ = self.blstm(x)
        # print("x.data.size() after self.blstm ", x.data.size())

        if is_train:
            x, _ = pad_packed_sequence(x, batch_first=True)
            # print("is_train triggered ", x.data.size())
        x = self.dropout(x)

        # B x T x hidden -> B x T x FD
        # print("x.data.size() before self.linear ", x.data.size())
        x = self.linear(x)
        # print("x.data.size() after self.linear ", x.data.size())

        x = self.activation(x)
        # print("x.data.size() after self.activation ", x.data.size())

        B = x.shape[0]
        if is_train:
            # B x TF x D
            x = x.view(B, -1, self.D)
        else:
            # B x TF x D -> TF x D
            x = x.view(-1, self.D)

        return x


class DPCL_DPRNN(nn.Module):
    '''
        Implement of Deep Clustering with DPRNN version 0.0.1
    '''

    def __init__(self, in_channels, hidden_channels,
                 dropout=0.0, bidirectional=True, activation="Tanh",
                 rnn_type="LSTM", norm='ln', num_layers=6,
                 num_spks=2, emb_D=40,
                 K=250,
                 ):
        super(DPCL_DPRNN, self).__init__()
        self.emb_D = emb_D
        self.dprnn = Dual_Path_RNN(in_channels, hidden_channels,
                                   rnn_type, norm, dropout, bidirectional=True, num_layers=num_layers, K=K,
                                   num_spks=num_spks)
        self.dropout = nn.Dropout(dropout)
        self.activation = getattr(torch.nn, activation)()
        self.linear = nn.Linear(
            2*hidden_channels if bidirectional else hidden_channels, in_channels * emb_D)

        self.D = emb_D

    def forward(self, x, is_train=True):
        '''
           input: 
                  for train: B x T x F
                  for test: T x F
           return: 
                  for train: B x TF x D
                  for test: TF x D
        '''
        # B x T x F -> B x T x hidden
        # DPRNN takes x and outputs x with same shape
        x = self.dprnn(x, is_train=is_train)

        if is_train:
            # It gets transformed back to a 3 dim tensor here [B, T, F]
            x, _ = pad_packed_sequence(x, batch_first=True)
        x = self.dropout(x)
        x = x.permute(0, 2, 1)
        # B x T x hidden -> B x T x FD
        x = self.linear(x)
        x = self.activation(x)
        B = x.shape[0]
        if is_train:
            # B x TF x D
            x = x.view(B, -1, self.D)
        else:
            # B x TF x D -> TF x D
            x = x.view(-1, self.D)

        return x


class GlobalLayerNorm(nn.Module):
    '''
       Calculate Global Layer Normalization
       dim: (int or list or torch.Size) –
          input shape from an expected input of size
       eps: a value added to the denominator for numerical stability.
       elementwise_affine: a boolean value that when set to True,
          this module has learnable per-element affine parameters
          initialized to ones (for weights) and zeros (for biases).
    '''

    def __init__(self, dim, shape, eps=1e-8, elementwise_affine=True):
        super(GlobalLayerNorm, self).__init__()
        self.dim = dim
        self.eps = eps
        self.elementwise_affine = elementwise_affine

        if self.elementwise_affine:
            if shape == 3:
                self.weight = nn.Parameter(torch.ones(self.dim, 1))
                self.bias = nn.Parameter(torch.zeros(self.dim, 1))
            if shape == 4:
                self.weight = nn.Parameter(torch.ones(self.dim, 1, 1))
                self.bias = nn.Parameter(torch.zeros(self.dim, 1, 1))
        else:
            self.register_parameter('weight', None)
            self.register_parameter('bias', None)

    def forward(self, x):
        # x = N x C x K x S or N x C x L
        # N x 1 x 1
        # cln: mean,var N x 1 x K x S
        # gln: mean,var N x 1 x 1
        if x.data.dim() == 4:
            mean = torch.mean(x, (1, 2, 3), keepdim=True)
            var = torch.mean((x-mean)**2, (1, 2, 3), keepdim=True)
            if self.elementwise_affine:
                x = self.weight*(x-mean)/torch.sqrt(var+self.eps)+self.bias
            else:
                x = (x-mean)/torch.sqrt(var+self.eps)
        if x.data.dim() == 3:
            mean = torch.mean(x, (1, 2), keepdim=True)
            var = torch.mean((x-mean)**2, (1, 2), keepdim=True)
            if self.elementwise_affine:
                x = self.weight*(x-mean)/torch.sqrt(var+self.eps)+self.bias
            else:
                x = (x-mean)/torch.sqrt(var+self.eps)
        return x


class CumulativeLayerNorm(nn.LayerNorm):
    '''
        Calculate Cumulative Layer Normalization
        dim: you want to norm dim
        elementwise_affine: learnable per-element affine parameters
    '''

    def __init__(self, dim, elementwise_affine=True):
        super(CumulativeLayerNorm, self).__init__(
            dim, elementwise_affine=elementwise_affine, eps=1e-8)

    def forward(self, x):
        # x: N x C x K x S or N x C x L
        # N x K x S x C
        if x.data.dim() == 4:
            x = x.permute(0, 2, 3, 1).contiguous()
            # N x K x S x C == only channel norm
            x = super().forward(x)
            # N x C x K x S
            x = x.permute(0, 3, 1, 2).contiguous()
        if x.data.dim() == 3:
            x = torch.transpose(x, 1, 2)
            # N x L x C == only channel norm
            x = super().forward(x)
            # N x C x L
            x = torch.transpose(x, 1, 2)
        return x


def select_norm(norm, dim, shape):
    if norm == 'gln':
        return GlobalLayerNorm(dim, shape, elementwise_affine=True)
    if norm == 'cln':
        return CumulativeLayerNorm(dim, elementwise_affine=True)
    if norm == 'ln':
        return nn.GroupNorm(1, dim, eps=1e-8)
    else:
        return nn.BatchNorm1d(dim)


class Dual_RNN_Block(nn.Module):  # Corresponds to only B) # This block is standalone
    '''
       Implementation of the intra-RNN and the inter-RNN
       input:
            in_channels: The number of expected features in the input x
            out_channels: The number of features in the hidden state h
            rnn_type: RNN, LSTM, GRU
            norm: gln = "Global Norm", cln = "Cumulative Norm", ln = "Layer Norm"
            dropout: If non-zero, introduces a Dropout layer on the outputs 
                     of each LSTM layer except the last layer, 
                     with dropout probability equal to dropout. Default: 0
            bidirectional: If True, becomes a bidirectional LSTM. Default: False
    '''

    def __init__(self, in_channels,
                 hiddden_cells, rnn_type='LSTM', norm='gln',
                 dropout=0, bidirectional=False, num_spks=2):
        super(Dual_RNN_Block, self).__init__()
        # self.intra_rnn = nn.LSTM(args, **kwargs)
        self.intra_rnn = getattr(nn, rnn_type)(
            input_size=hiddden_cells*2 if bidirectional else hiddden_cells, hidden_size=hiddden_cells,
            num_layers=1, batch_first=True, dropout=dropout, bidirectional=bidirectional)
        self.inter_rnn = getattr(nn, rnn_type)(
            input_size=hiddden_cells*2 if bidirectional else hiddden_cells, hidden_size=hiddden_cells,
            num_layers=1, batch_first=True, dropout=dropout, bidirectional=bidirectional)
        # Norm
        self.intra_norm = select_norm(
            norm, hiddden_cells*2 if bidirectional else hiddden_cells, 4)  # in the
        self.inter_norm = select_norm(
            norm, hiddden_cells*2 if bidirectional else hiddden_cells, 4)  # in the
        # Linear
        self.intra_linear = nn.Linear(
            hiddden_cells*2 if bidirectional else hiddden_cells,  hiddden_cells*2 if bidirectional else hiddden_cells)
        self.inter_linear = nn.Linear(
            hiddden_cells*2 if bidirectional else hiddden_cells,  hiddden_cells*2 if bidirectional else hiddden_cells)

    def forward(self, x):
        '''
         B: BATCH
         N: feature dims 
         K: Length of the chunks (from L length of segment) 
         S: Number of chunks
           x: [B, N, K, S]
           out: [Spks, B, N, K, S]
        '''
        B, N, K, S = x.shape
        # [BS, K, N] # Preparing the shape to feed into the intra chunk(?)
        intra_rnn = x.permute(0, 3, 2, 1).contiguous().view(B*S, K, N)
        # [BS, K, H]
        # Gets the type of rnn then feeds the data
        intra_rnn, _ = self.intra_rnn(intra_rnn)
        # [BS, K, N]
        intra_rnn = self.intra_linear(
            intra_rnn.contiguous().view(B*S*K, -1)).view(B*S, K, -1)

        # [B, S, K, N]
        intra_rnn = intra_rnn.view(B, S, K, -1)  # Infer the correct size N

        # [B, N, K, S]
        intra_rnn = intra_rnn.permute(0, 3, 2, 1).contiguous()
        intra_rnn = self.intra_norm(intra_rnn)

        # [B, N, K, S]
        # adds the processed input back to the original input
        intra_rnn = intra_rnn + x

        # inter RNN
        # [BK, S, N] # Prepares shape, note 2 and 3 are exchanged this time
        inter_rnn = intra_rnn.permute(0, 2, 3, 1).contiguous().view(B*K, S, N)
        # [BK, S, H]
        # Gets the type of rnn then feeds the data
        inter_rnn, _ = self.inter_rnn(inter_rnn)

        # [BK, S, N]
        inter_rnn = self.inter_linear(
            inter_rnn.contiguous().view(B*S*K, -1)).view(B*K, S, -1)

        # [B, K, S, N]
        inter_rnn = inter_rnn.view(B, K, S, N)
        # [B, N, K, S]
        inter_rnn = inter_rnn.permute(0, 3, 1, 2).contiguous()
        inter_rnn = self.inter_norm(inter_rnn)
        # [B, N, K, S]
        # intra_rnn (tensor) is the "original" input that was fed to the inter rnn (layers)
        out = inter_rnn + intra_rnn

        return out


class Dual_Path_RNN(nn.Module):  # The DPRNN block all together
    '''
       Implementation of the Dual-Path-RNN model 
       input:
            in_channels: The number of expected features in the input x
            out_channels: The number of features in the hidden state h
            rnn_type: RNN, LSTM, GRU
            norm: gln = "Global Norm", cln = "Cumulative Norm", ln = "Layer Norm"
            dropout: If non-zero, introduces a Dropout layer on the outputs 
                     of each LSTM layer except the last layer, 
                     with dropout probability equal to dropout. Default: 0
            bidirectional: If True, becomes a bidirectional LSTM. Default: False
            num_layers: number of Dual-Path-Block
            K: the length of chunk
            num_spks: the number of speakers
    '''

    def __init__(self, in_channels, hidden_channels,
                 rnn_type='LSTM', norm='ln', dropout=0,
                 bidirectional=False, num_layers=4, K=200, num_spks=2):
        super(Dual_Path_RNN, self).__init__()
        self.K = K
        self.num_spks = num_spks
        self.num_layers = num_layers
        self.norm = select_norm(norm, in_channels, 3)
        self.linear_2_hidden = nn.Linear(
            in_channels, 2*hidden_channels if bidirectional else hidden_channels)

        self.dual_rnn = nn.ModuleList([])
        for i in range(num_layers):
            self.dual_rnn.append(Dual_RNN_Block(in_channels, hidden_channels,
                                                rnn_type=rnn_type, norm=norm, dropout=dropout,
                                                bidirectional=bidirectional,))

    def forward(self, x, is_train=True):
        '''
           x: [B, N, L]

        '''
        # Current [BT, F]
        x = self.norm(x)

        # transform into [B, T(L), F(N)]
        if is_train:
            x, _ = pad_packed_sequence(x, batch_first=True)
        else:
            x = torch.unsqueeze(x, 0)
        # [B, N, L]
        x = self.linear_2_hidden(x)
        # [B, N, K, S]
        x = x.data.permute(0, 2, 1).contiguous()
        x, gap = self._Segmentation(x, self.K)
        # [B, N*spks, K, S]
        for i in range(self.num_layers):  # its gonna make 6 instances of a dprnn block
            x = self.dual_rnn[i](x)
        # [B*spks, N, K, S]
        B, N, K, S = x.shape

        # [B*spks, N, L]
        x = self._over_add(x, gap)

        x = x.permute(0, 1, 2).contiguous()

        if is_train:
            x = pack_sequence(x)
        return x

    def _padding(self, input, K):
        '''
           padding the audio times
           K: length of chunks
           P: hop size
           input: [B, N, L] # N = feature dims, L=Length of segment
        '''
        B, N, L = input.shape
        P = K // 2
        gap = K - (P + L % K) % K
        if gap > 0:
            pad = torch.Tensor(torch.zeros(B, N, gap)).type(input.type())
            input = torch.cat([input, pad], dim=2)

        _pad = torch.Tensor(torch.zeros(B, N, P)).type(input.type())
        input = torch.cat([_pad, input, _pad], dim=2)

        return input, gap

    def _Segmentation(self, input, K):  # Corresponds to A)
        '''
           the segmentation stage splits
           K: chunks of length
           P: hop size
           input: [B, N, L]
           output: [B, N, K, S]
        '''
        B, N, L = input.shape
        P = K // 2
        # padding may not be needed, as the input would have gone through pre processing with STFT
        input, gap = self._padding(input, K)
        # [B, N, K, S]
        input1 = input[:, :, :-P].contiguous().view(B, N, -1, K)
        input2 = input[:, :, P:].contiguous().view(B, N, -1, K)
        input = torch.cat([input1, input2], dim=3).view(
            B, N, -1, K).transpose(2, 3)  # transforms into 3D tensor

        return input.contiguous(), gap

    def _over_add(self, input, gap):  # Corresponds to C)
        '''
           Merge sequence
           input: [B, N, K, S]
           gap: padding length
           output: [B, N, L]
        '''
        B, N, K, S = input.shape
        P = K // 2
        # [B, N, S, K]
        input = input.transpose(2, 3).contiguous().view(B, N, -1, K * 2)

        input1 = input[:, :, :, :K].contiguous().view(B, N, -1)[:, :, P:]
        input2 = input[:, :, :, K:].contiguous().view(B, N, -1)[:, :, :-P]
        input = input1 + input2
        # [B, N, L]
        if gap > 0:
            input = input[:, :, :-gap]

        return input
