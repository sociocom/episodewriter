<template>
    <div>
        <form @submit.prevent="submitForm">
            <label for="text">Enter prompt:</label>
            <input type="text" id="text" v-model="text" required>
            <button type="submit">Submit</button>
        </form>
        <img v-if="imageUrl" :src="imageUrl" alt="Image">
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            text: '',
            imageUrl: ''
        };
    },
    methods: {
        submitForm() {
            axios.get('/episodewriter/api/image_generation', {
                params: {
                    prompt: this.text
                },
                responseType: 'blob', 
                cache: false})
                .then(response => {
                    console.log(response);
                    this.imageUrl = URL.createObjectURL(response.data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }
};
</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

.form {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.input {
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 300px;
}

.button {
    padding: 0.5rem 1rem;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.image {
    margin-top: 1rem;
    max-width: 100%;
    height: auto;
}

</style>