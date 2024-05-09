<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import ImageForm from './components/ImageForm.vue'
import ImageCaptionDisplay from './components/ImageCaptionDisplay.vue';
</script>

<template>
  <v-layout class="rounded rounded-md">
    <v-app-bar color="secondary">
      <v-spacer></v-spacer>
      <h2>EpisodeWriter</h2>
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-main class="d-flex align-center justify-center" style="min-width: 800px;">
      <v-row align="center" justify="center">
        <v-col cols="6">
          <ImageForm/>
        </v-col>
        <v-col cols="6">
          <ImageCaptionDisplay />
        </v-col>
      </v-row>
    </v-main>
  </v-layout>
</template>

<style scoped>
</style>