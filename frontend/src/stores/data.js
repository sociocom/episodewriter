import { defineStore } from 'pinia';

export const useDataStore = defineStore({
  id: 'imageStore',
  state: () => ({
    image: null,
    caption: '',
  }),
  actions: {
    setImage(image) {
      this.image = image;
    },
    setCaption(caption) {
      this.caption = caption;
    },
  },
});