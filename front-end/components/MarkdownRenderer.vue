<template>
    <div v-html="renderedMarkdown"></div>
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