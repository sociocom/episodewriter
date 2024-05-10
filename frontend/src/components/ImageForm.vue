<template>
    <v-layout class="layout">
        <form @submit.prevent="submitForm">
            <v-textarea
                bg-color="grey-lighten-3"
                color="secondary"
                label="Text"
                v-model="text"
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
        </form>

        
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
    
    // Show the task progress
    const taskId = ref(null);
    const intervalId = ref(null);
    const totalIterations = ref(0); 
    const currentIteration = ref(0);  
    const running = ref(false);

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
        console.log(response);
        totalIterations.value = response.data.total_iterations;
        currentIteration.value = response.data.current_iteration;
        console.log(response.data.state)
        if (response.data.state === 'SUCCESS') {
          // The task is done, clear the interval
          clearInterval(intervalId.value);
          // Do something with the result
          console.log(response.data)

          axios.get(`/episodewriter/api/get_image/${taskId.value}`, {
            responseType: 'blob',
          })
          .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            console.log(url)
            imageUrl.value = url;
            dataStore.setImage(imageUrl.value);
            dataStore.setCaption(text.value);
            running.value = false;
          });

        }
      });
    };

    

    const submitForm = () => {
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
        console.log(response);
        taskId.value = response.data.task_id;
        running.value = true;

        setTimeout(() => {
          intervalId.value = setInterval(checkTaskStatus, 1000);
        }, 500);
        
        // imageUrl.value = URL.createObjectURL(response.data);
        // dataStore.setImage(imageUrl.value);
        // dataStore.setCaption(text.value);
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
    };
  },
};
</script>