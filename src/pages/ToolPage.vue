<template>
  <q-page class="flex flex-center" style="gap: 150px">
    <!--RNN Model-->
    <div class="base-model">
      <h5 class="q-my-none">Deep Clustering with Recurrent Neural Network</h5>
      <!--Input Container-->
      <div class="q-mt-lg" style="width: 500px">
        <!--Upload file button-->
        <q-input
          v-if="!rnn_togglebtn"
          class="custom-file-input q-py-none q-mb-md"
          type="file"
          filled
          bottom-slots
          v-model="rnn_media"
          label="Upload File"
          :dense="dense"
          accept=".mp3"
        >
          <template v-slot:prepend>
            <q-icon name="upload" @click.stop.prevent />
          </template>
          <template v-slot:append>
            <q-icon
              name="close"
              @click.stop.prevent="media = null"
              class="cursor-pointer"
            />
          </template>
        </q-input>

        <!--Toggle to this button when file is inputted-->
        <q-file
          v-else
          class="custom-upload-btn"
          multiple
          filled
          bottom-slots
          v-model="rnn_media"
          label="Upload File"
          :readonly="rnn_togglebtn"
          accept=".mp3"
        >
          <template v-slot:prepend>
            <q-icon name="upload" @click.stop.prevent />
          </template>
          <template v-slot:append>
            <q-icon
              name="close"
              @click.stop.prevent="rnn_media = null"
              class="cursor-pointer"
            />
          </template>
        </q-file>

        <!--Mixed Audio Media Player-->
        <div class="flex justify-end" style="width: 450px">
          <div class="mixed-player-box q-pa-md">
            <p class="q-my-none text-subtitle1">Mixed Audio</p>
            <q-media-player
              class="custom-player"
              ref="rnn_mediaplayer"
              type="audio"
              style="border-radius: 3px"
            >
            </q-media-player>
          </div>
          <!--Separate Button-->
          <q-btn
            class="separate-btn q-mt-sm"
            no-caps
            square
            label="Separate"
            :disabled="!rnn_togglebtn"
          />
        </div>
      </div>

      <!--Output Container-->
      <div class="q-mt-md">
        <h6 class="q-my-none">Output</h6>
        <div class="col justify-end" style="width: 450px">
          <div class="mixed-player-box q-pa-md">
            <p class="q-my-none text-subtitle1">Separated Audio 1</p>
            <q-media-player
              class="custom-player"
              ref=""
              type="audio"
              :sources="sources"
              style="border-radius: 3px"
            >
            </q-media-player>

            <p class="q-my-none q-mt-md text-subtitle1">Separated Audio 2</p>
            <q-media-player
              class="custom-player"
              ref=""
              type="audio"
              :sources="sources"
              style="border-radius: 3px"
            >
            </q-media-player>
          </div>
        </div>
      </div>
    </div>

    <!--DPRNN Model-->
    <div class="our-model">
      <h5 class="q-my-none">
        Deep Clustering with Dual-Path Recurrent Neural Network
      </h5>
      <!--Input Container-->
      <div class="q-mt-lg" style="width: 500px">
        <!--Upload file button-->
        <q-input
          v-if="!dprnn_togglebtn"
          class="custom-file-input q-py-none q-mb-md"
          type="file"
          filled
          bottom-slots
          v-model="dprnn_media"
          label="Upload File"
          :dense="dense"
          accept=".mp3"
        >
          <template v-slot:prepend>
            <q-icon name="upload" @click.stop.prevent />
          </template>
          <template v-slot:append>
            <q-icon
              name="close"
              @click.stop.prevent="media = null"
              class="cursor-pointer"
            />
          </template>
        </q-input>

        <!--Toggle to this button when file is inputted-->
        <q-file
          v-else
          class="custom-upload-btn"
          multiple
          filled
          bottom-slots
          v-model="dprnn_media"
          label="Upload File"
          :readonly="dprnn_togglebtn"
          accept=".mp3"
        >
          <template v-slot:prepend>
            <q-icon name="upload" @click.stop.prevent />
          </template>
          <template v-slot:append>
            <q-icon
              name="close"
              @click.stop.prevent="dprnn_media = null"
              class="cursor-pointer"
            />
          </template>
        </q-file>

        <!--Mixed Audio Media Player-->
        <div class="flex justify-end" style="width: 450px">
          <div class="mixed-player-box q-pa-md">
            <p class="q-my-none text-subtitle1">Mixed Audio</p>
            <q-media-player
              class="custom-player"
              ref="dprnn_mediaplayer"
              type="audio"
              style="border-radius: 3px"
            >
            </q-media-player>
          </div>
          <!--Separate Button-->
          <q-btn
            class="separate-btn q-mt-sm"
            no-caps
            square
            label="Separate"
            :disabled="!dprnn_togglebtn"
          />
        </div>
      </div>

      <!--Output Container-->
      <div class="q-mt-md">
        <h6 class="q-my-none">Output</h6>
        <div class="col justify-end" style="width: 450px">
          <div class="mixed-player-box q-pa-md">
            <p class="q-my-none text-subtitle1">Separated Audio 1</p>
            <q-media-player
              class="custom-player"
              ref=""
              type="audio"
              :sources="sources"
              style="border-radius: 3px"
            >
            </q-media-player>

            <p class="q-my-none q-mt-md text-subtitle1">Separated Audio 2</p>
            <q-media-player
              class="custom-player"
              ref=""
              type="audio"
              :sources="sources"
              style="border-radius: 3px"
            >
            </q-media-player>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style lang="scss">
@import "src/pages/styles/ToolPage.scss";
</style>

<script>
import { ref, watch } from "vue";
import { QMediaPlayer } from "@quasar/quasar-ui-qmediaplayer";
import "@quasar/quasar-ui-qmediaplayer/src/index.sass";

export default {
  components: {
    QMediaPlayer,
  },
  setup() {
    const rnn_media = ref(null);
    const rnn_mediaplayer = ref(null);
    const rnn_togglebtn = ref(false);

    const dprnn_media = ref(null);
    const dprnn_mediaplayer = ref(null);
    const dprnn_togglebtn = ref(false);

    const itemUrl = ref(null);

    //This is just for testing
    const sources = [
      {
        src: "",
        type: "audio/mp3",
      },
    ];

    watch(
      () => rnn_media.value,
      (file) => {
        if (file && file.length > 0) {
          console.log(file);
          rnn_togglebtn.value = true;
          loadFileBlob(file, 0);
        } else {
          rnn_togglebtn.value = false;
          loadFileBlob(null, 0);
        }
      }
    );

    watch(
      () => dprnn_media.value,
      (file) => {
        if (file && file.length > 0) {
          dprnn_togglebtn.value = true;
          loadFileBlob(file, 1);
        } else {
          dprnn_togglebtn.value = false;
          loadFileBlob(null, 1);
        }
      }
    );

    function loadFileBlob(file, num) {
      if (num == 0) {
        rnn_mediaplayer.value.loadFileBlob(file);
      } else {
        dprnn_mediaplayer.value.loadFileBlob(file);
      }
    }

    return {
      //for RNN
      rnn_media,
      rnn_mediaplayer,
      rnn_togglebtn,

      //for DPRNN
      dprnn_media,
      dprnn_mediaplayer,
      dprnn_togglebtn,

      itemUrl,
      sources,
    };
  },
};
</script>
