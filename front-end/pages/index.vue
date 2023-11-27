<template>
    <div class="flex justify-end">

        <!-- <UContainer class="bg-red-500">
            <Placeholder class="h-32" />
        </UContainer> -->
        
        <div id="chat-box" class="h-screen w-[80%] px-10 bg-gray-800 flex flex-col gap-3 items-center">
            <div id="chat-header" class="border-b-2 w-full">
                <h2 class="text-2xl">Chat</h2>
            </div>

            <div id="chat-body" class="flex flex-col gap-2 overflow-x-auto h-full w-2/3">
                <ContentRenderer v-for="message in chatMessages" :value="message['content']" 
                :class="message.role === 'assistant' ? 'self-start' : 'self-end border-primary'" >
                </ContentRenderer>
            </div>

            <UTextarea color="primary" variant="outline" placeholder="Search..." :rows="4"
            v-model="inputText" @keydown.enter="sendInput"
            class="w-2/3 self-center" />
        </div>

    </div>
</template>

<script setup>
const inputText = ref('')
const chatMessages = ref([])

const sendInput = (event) => {
    event.preventDefault()

    let message = { role: 'user', content: inputText.value }
    chatMessages.value.push(message)

    inputText.value = ''
    console.log(chatMessages.value)
}

</script>