<template>
    <div id="chat-box" class="h-screen w-5/6 px-10 bg-gray-800 flex flex-col gap-3 items-center text-gray-100">

        <div id="chat-header" class="w-full border-b-2 flex justify-between py-2 mt-5">
            <h2 class="text-2xl">{{ name }}</h2>
            <UButton @click="renameConversation">Rename</UButton>
        </div>

        <div @scroll="logScroll" ref="chatBody" id="chat-body" class="w-full flex flex-col gap-2 overflow-y-scroll h-full">

            <div v-for="message in chatMessages" :class="message['role'] + '-messages'">
                <MarkdownRenderer v-if="message['role'] == 'assistant'" :markdown="message['content']" class="" />
                <div v-else class="flex px-5 gap-3 py-3">
                    <Icon name="material-symbols:person-2-rounded" class="w-32 h-32" />
                    <p class=" text-xl">{{ message['content'] }}</p>
                </div>

            </div>
        </div>

        <UTextarea color="gray" variant="outline" placeholder="Prompt..." :rows="4"
        v-model="inputText" @keydown.enter="signalInputReady" :disabled="name == 'None'"
        class="w-2/3 self-center text-white mb-10" />
    </div>

</template>

<script setup>

const inputText = ref('')
const chatBody = ref(null)

const props = defineProps({
    chatMessages: {
        type: Array,
        default: []
    },
    name: {
        type: String,
        default: ''
    },
    socket: {
        type: Object,
        default: {}
    }
})

const emit = defineEmits(['input-ready', 'request-rename'])

const signalInputReady = (event) => {
    if (event.key == 'Enter' && event.shiftKey || inputText.value == '' ) return
    event.preventDefault()

    emit('input-ready', inputText.value)

    inputText.value = ''

}

const scrollToLast = () => {
    setTimeout(() => {
        const container = chatBody.value
        if (container) {
            const children = container?.children
            const lastMessageElement = children[children.length - 1]
            if (lastMessageElement) {
                lastMessageElement.scrollIntoView({  block: 'end' });
            }
        }
    }, 100);
}

const lastMessageElement = computed(() => {
    const children = chatBody.value?.children
    return children ? children[children.length - 1] : null
})

const logScroll = (event) => {
    console.log(event.target.scrollTop + event.target.offsetHeight, event.target.scrollHeight, event.target.offsetHeight)
}

watch(() => props.chatMessages.length, () => {
    scrollToLast()
    console.log('chat messages changed')
})

const renameConversation = () => {
    emit('request-rename')
}


</script>

<style scoped>
.user-messages {
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 10px 0;
    max-width: 75%;

}
</style>