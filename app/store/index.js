export const state = () => ({
    active_chat_user: null,
    active_chat_user_id: null,
    active_chat_user_image: null,
    users: [],
    conversation: [],
});

export const getters = {
    conversation: (state) => state.conversation,
};

export const mutations = {
    // Toggling the chat to active after selecting
    toggleSelected(state, user) {
        state.active_chat_user = user;
        state.active_chat_user_id = user.user_id;
        state.active_chat_user_image = user.image;
    },

    // For sending of message
    sendMessage(state, message) {
        state.conversation.push(message);
    },

    updconversation(state, conversation) {
        state.conversation = conversation;
    },
};

export const actions = {
    async updateConversation({ commit }, user) {
        let currentUser = this.$auth.user.username;
        try {
            this.$fire.firestore
                .collection("message")
                .orderBy("createdAt")
                .onSnapshot((querySnapshot) => {
                    var allMessages = [];
                    querySnapshot.forEach((doc) => {
                        let sender = doc.data().sender;
                        let receiver = doc.data().receiver;

                        if (sender == user.username && receiver == currentUser) {
                            allMessages.push(doc.data());
                        }

                        if (sender == currentUser && receiver == user.username) {
                            allMessages.push(doc.data());
                        }
                    });

                    commit("updconversation", allMessages);
                });
        } catch (e) {
            console.error(e);
        }
    },
};
