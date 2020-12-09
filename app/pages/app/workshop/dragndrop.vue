<template>
    <v-sheet
        id="dropzone"
        ref="dzone"
        tabindex="0"
        title="Click to grap a file from your PC!"
        color="indigo lighten-4"
        width="100%"
        style="cursor: pointer"
        height="200"
        class="pa-2"
    >
        <input ref="upload" id="fileUpload" type="file" accept="text/xml" style="display: none" />
        <v-row justify="center">
            <v-icon v-if="!dragover" color="indigo darken-2" size="75"
                >mdi-cloud-upload-outline</v-icon
            >
            <v-icon v-if="dragover" color="indigo darken-2" size="75">mdi-book-plus</v-icon>
        </v-row>
        <v-row justify="center">
            <span class="title indigo--text text--darken-2"
                >Drag'n drop or click to upload file!</span
            >
        </v-row>
    </v-sheet>
</template>

<script>
export default {
    middleware: ["auth"],
};
</script>
