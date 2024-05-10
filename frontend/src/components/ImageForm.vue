<template>
    <v-layout class="layout">
        <v-form ref="form" @submit.prevent="submitForm">
            <v-textarea
                bg-color="grey-lighten-3"
                color="secondary"
                label="Text"
                v-model="text"
                :rules="rules"
            ></v-textarea>
            <v-btn color="secondary" @click="submitForm" v-bind:disabled="running">Submit</v-btn>
            <div style="background-color: white;">
            <br/>
            <v-progress-linear
              v-if="running"
              :model-value="progress"
              color="secondary"
              height="20"
              striped
            ></v-progress-linear>
            </div>
        </v-form>

        
    </v-layout>
</template>

<script>
import axios from 'axios';
import { ref, computed } from 'vue';
import { useDataStore } from '@/stores/data.js';

export default {
  setup() {
    const dataStore = useDataStore();
    const text = ref('');
    const imageUrl = ref('');
    const valid = false;
    
    // Show the task progress
    const taskId = ref(null);
    const intervalId = ref(null);
    const totalIterations = ref(0); 
    const currentIteration = ref(0);  
    const running = ref(false);

    const form = ref(null);
    const formValid = computed(() => {
      if (form.value) {
        return form.value.validate().then(valid => valid);
      }
      return false;
    });

    const rules = ref([
      value => !!value || 'Text must not be empty.',
      value => /[\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\uFF00-\uFFEF\u4E00-\u9FAF]/.test(value) || 'Text must be in Japanese.',
    ]);

    const progress = computed(() => {
      if (totalIterations.value === 0) {
        return 0;
      }
      return (currentIteration.value / totalIterations.value) * 100;
    });

    const checkTaskStatus = () => {
      axios.get(`/episodewriter/api/task_status/${taskId.value}`, {
        responseType: 'json',
      })
      .then(response => {
        totalIterations.value = response.data.total_iterations;
        currentIteration.value = response.data.current_iteration;
        if (response.data.state === 'SUCCESS') {
          clearInterval(intervalId.value);

          axios.get(`/episodewriter/api/get_image/${taskId.value}`, {
            responseType: 'blob',
          })
          .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            imageUrl.value = url;
            dataStore.setImage(imageUrl.value);
            dataStore.setCaption(text.value);
            running.value = false;
          });

        }
      });
    };

    const submitForm = () => {

      form.value.validate().then(result => {
        if (!result.valid) {
          // Form is not valid, do not submit it
          return;
        }
        // Form is valid, you can submit it      
        currentIteration.value = 0;
        totalIterations.value = 0;
        axios.get('/episodewriter/api/image_generation_task', {
          params: {
            prompt: text.value,
          },
          responseType: 'json',
          cache: false,
        })
        .then(response => {
          taskId.value = response.data.task_id;
          running.value = true;

          setTimeout(() => {
            intervalId.value = setInterval(checkTaskStatus, 1000);
          }, 500);
          
        });
      });
    };

    return {
      text,
      imageUrl,
      submitForm,
      taskId,
      totalIterations, 
      currentIteration,
      running,
      progress,
      form,
      formValid,
      rules, 
      valid,
    };
  },
};
</script>