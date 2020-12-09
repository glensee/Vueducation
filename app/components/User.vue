<template>
    <div
        class="user-container"
        :class="{ active_chat: user.user_id === active_chat_user_id }"
        @click="toggle()"
    >
        <div class="user">
            <div class="user-image">
                <img :src="getImage(user.image)" v-bind:alt="user.image" />
            </div>
            <div class="user-info">
                <h5>{{ user.username }}</h5>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
    name: "User",
    props: ["user"],

    // Getting the values from Store
    computed: {
        ...mapState({
            active_chat_user_id: (state) => state.active_chat_user_id,
            active_chat_user_image: (state) => state.active_chat_user_image,
        }),
    },

    methods: {
        ...mapMutations({
            toggleSelected: "toggleSelected",
        }),

        ...mapActions({
            update: "updateConversation",
        }),

        getImage(image) {
            return require("../assets/profile/" + image);
        },

        // Calling the mapped function 'toggleSelected' mutation
        toggle() {
            this.toggleSelected(this.user);
            this.update(this.user);
        },
    },
};
</script>

<style></style>
