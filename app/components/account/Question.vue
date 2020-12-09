<template>
    <v-list-item class="question" :to="path">
        <v-list-item-content>
            <h2>{{ title }}</h2>
            <p>{{ question }}</p>
        </v-list-item-content>
    </v-list-item>
</template>

<script>
export default {
    name: "Question",
    props: ["question", "title", "path"],
};
</script>

<style>
.question {
    padding: 1rem;
    border: 1px dotted #ccc;
    margin: 1rem 0;
}
</style>
