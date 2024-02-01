<template>
    <div id="chat-box" class="h-screen w-[80%] px-10 bg-gray-800 flex flex-col gap-3 items-center">
        <div id="chat-header" class="border-b-2 w-full">
            <h2 class="text-2xl">Chat</h2>
        </div>

        <div id="chat-body" class="flex flex-col gap-2 overflow-x-auto h-full w-2/3">
            

            <div v-for="message in chatMessages">
                <MarkdownRenderer v-if="message['role'] == 'assistant'" :value="message['content']" >
                </MarkdownRenderer>
                <p v-else >{{ message['content'] }}</p>
            </div>
        </div>

        <UTextarea color="primary" variant="outline" placeholder="Search..." :rows="4"
        v-model="inputText" @keydown.enter="signalInputReady"
        class="w-2/3 self-center" />
    </div>

</template>

<script setup>

const inputText = ref('')

const props = defineProps({
    chatMessages: {
        type: Array,
        default: []
    }
})

const emit = defineEmits(['input-ready'])

const signalInputReady = (event) => {
    event.preventDefault()

    emit('input-ready', inputText.value)

    inputText.value = ''

}

</script>