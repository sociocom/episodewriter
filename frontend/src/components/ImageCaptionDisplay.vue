<template>
    <div class="">
      <img :src="image" alt="Image from store" v-if="image" />
      <p class="caption">
        {{ caption }}
      </p>
      <v-btn class="download-button" color="secondary" :href="image" download="image.jpeg" v-if="image">Download Image</v-btn>
    </div>
  </template>
  
  <script>
  import { computed } from 'vue';
  import { useDataStore } from '@/stores/data.js';
  
  export default {
    name: 'ImageCaptionDisplay',
    setup() {
      const dataStore = useDataStore();
      return {
        image: computed(() => dataStore.image),
        caption: computed(() => dataStore.caption),
      };
    },
  };
  </script>
<style scoped>
img {
  height:70vh;
}

.caption {
  color: black;
  text-align: left;
  font-size: 1.8em;
}

.download-button {
  align-self: flex-end;
}

</style>