export const state = () =>({

    toggleSidebar: false

})

// mutations
export const mutations = {

    toggle(state) {
        state.toggleSidebar = !state.toggleSidebar
    },

    close(state) {
        state.toggleSidebar = false
    }

}


export const getters = {
    getToggleSideBar(state){
        return state.toggleSidebar
    }

}