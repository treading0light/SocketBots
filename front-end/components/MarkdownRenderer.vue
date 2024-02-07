<template>
    <div class="ai-markdown m-auto prose prose-2xl prose-slate prose-invert" v-html="renderedMarkdown"></div>
</template>

<script setup>
import MarkdownIt from 'markdown-it'

const props = defineProps({
    markdown: String
})

const renderedMarkdown = computed(() => {
    const md = new MarkdownIt();
    return md.render(props.markdown);
})

</script>

<style scoped>
.ai-markdown {
    font-family: 'Oswald', sans-serif;
}
</style>