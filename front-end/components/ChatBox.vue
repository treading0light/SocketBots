<template>
    <div id="chat-box" class="h-screen w-5/6 px-10 bg-gray-800 flex flex-col gap-3 items-center text-gray-100">

        <div id="chat-header" class="w-full border-b-2 flex justify-between mt-5">
            <h2 class="text-2xl">{{ name }}</h2>
            <UButton @click="renameConversation">Rename</UButton>
        </div>

        <div id="chat-body" class="flex flex-col gap-2 overflow-y-auto h-full">

            <div v-for="message in chatMessages" :class="message['role'] + '-messages'">
                <MarkdownRenderer v-if="message['role'] == 'assistant'" :markdown="message['content']" class="" />
                <div v-else class="flex px-5 gap-3 py-3">
                    <Icon name="material-symbols:person-2-rounded" class="w-32 h-32" />
                    <p class=" text-xl">{{ message['content'] }}</p>
                </div>

            </div>
        </div>

        <UTextarea color="gray" variant="outline" placeholder="Prompt..." :rows="4"
        v-model="inputText" @keydown.enter="signalInputReady"
        class="w-2/3 self-center text-white mb-10" />
    </div>

</template>

<script setup>

const inputText = ref('')

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

const emit = defineEmits(['input-ready', 'rename-conversation'])

const signalInputReady = (event) => {
    event.preventDefault()

    emit('input-ready', inputText.value)

    inputText.value = ''

}

const renameConversation = () => {
    emit('rename-conversation')
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