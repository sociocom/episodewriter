<template>
    <div>
      <img :src="image" alt="Image from store" v-if="image" />
      <p>{{ caption }}</p>
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