<template>
    <v-layout class="layout">
        <form @submit.prevent="submitForm">
            <v-textarea
                bg-color="grey-lighten-3"
                color="secondary"
                label="Text"
                v-model="text"
            ></v-textarea>
            <v-btn color="secondary" type="submit">Submit</v-btn>
        </form>
    </v-layout>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import { useDataStore } from '@/stores/data.js';

export default {
  setup() {
    const dataStore = useDataStore();
    const text = ref('');
    const imageUrl = ref('');

    const submitForm = () => {
      axios.get('/episodewriter/api/image_generation', {
        params: {
          prompt: text.value,
        },
        responseType: 'blob',
        cache: false,
      })
      .then(response => {
        console.log(response);
        imageUrl.value = URL.createObjectURL(response.data);
        dataStore.setImage(imageUrl.value);
        dataStore.setCaption(text.value);
      });
    };

    return {
      text,
      imageUrl,
      submitForm,
    };
  },
};
</script>