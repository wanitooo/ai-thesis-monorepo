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
          accept=".wav"
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
            @click="handleDRNNSeparate"
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
            @click="handler"
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
// import * as fs from "node:fs";
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
    const mixed_audio_path = ref(null);
    const speaker1_audio_path = ref(null);
    const speaker2_audio_path = ref(null);
    const itemUrl = ref(null);

    //This is just for testing
    const sources = [
      {
        src: "backend/media/separated/drnn/spk1/1995-1837-0027_4970-29095-0022",
        type: "audio/wav",
      },
    ];

    watch(
      () => rnn_media.value,
      async (file) => {
        if (file && file.length > 0) {
          console.log("file ", " TYPE: ", typeof file, file);
          rnn_togglebtn.value = true;
          const formData = new FormData();
          formData.append("file", file[0]);
          try {
            const res = await fetch("http://127.0.0.1:8000/upload-file/", {
              method: "POST",
              // headers: {
              //   'Content-Type': "multipart/form-data"
              // },
              body: formData,
            }).then((res) => res.json());
            console.log("fetch triggered, response ", res);
            mixed_audio_path.value = res.file;
            loadFileBlob(file, 0);
          } catch (error) {
            console.log("Something went wrong ", error);
          }
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
    async function handleDRNNSeparate() {
      console.log(
        "mixed_audio_path ",
        JSON.stringify({ file: mixed_audio_path.value })
      );
      const res = await fetch("http://127.0.0.1:8000/drnn-separate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ file: mixed_audio_path.value }),
      }).then((res) => res.json());
      console.log("Separate triggered, res ", res);
      speaker1_audio_path.value = res.spk_1;
      speaker2_audio_path.value = res.spk_2;
    }
    async function handler() {
      console.log("Triggered handler");
      // var output = fs.readFileSync("../../backend/requirements.txt");

      console.log(output);
    }
    return {
      //for RNN
      rnn_media,
      rnn_mediaplayer,
      rnn_togglebtn,
      handleDRNNSeparate,

      //for DPRNN
      dprnn_media,
      dprnn_mediaplayer,
      dprnn_togglebtn,
      handler,

      itemUrl,
      sources,
    };
  },
};
</script>
