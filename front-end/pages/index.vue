<template>
    <div class="flex justify-end">
        <SideNav @conversationSelected="selectConversation" :conversations="conversations" :currentConversation="currentConversation" :socket="socket" />
        <ChatBox :socket="socket" :chatMessages="currentConversation.messages" :name="currentConversation.name"
        @input-ready="sendInput" @rename-conversation="requestRename" />


    </div>
</template>

<script setup>
import { io } from "socket.io-client"
const config = useRuntimeConfig()
const socket = io(config.public.serverUrl)
const conversations = ref([])
const currentConversation = ref({"id": 0, "name": "None"})
const chatMessages = ref([])

const sendInput = (input) => {

    let message = { role: 'user', content: input, conversation_id: currentConversation.value.id }
    console.log(message)

    let messages = []
    if (chatMessages.value.length >= 3) {
        messages = chatMessages.value.slice(-3)
    } else {
        messages = chatMessages.value
    }

    messages.push(message)

    socket.emit('user-input', messages, currentConversation.value.id, (response) => {
        console.log('response from server' + JSON.stringify(response))
        chatMessages.value.push(response)
    })
}

const getMessages = (conversationId) => {
    socket.emit('get-messages', conversationId, (response) => {
        chatMessages.value = response
    })
}

const getAllConversations = () => {
    socket.emit('get-conversations', (response) => {
        conversations.value = response
        // emit('conversationSelected', conversations.value[0])
    })
}

const selectConversation = (conversation) => {
    currentConversation.value = conversation
}

const requestRename = () => {
    socket.emit('request-rename', currentConversation.value.id)
}

onMounted(() => {
    getAllConversations()
})

socket.on('connect', () => {
        console.log('Connected to server');
    })

socket.on('ai-output', (response) => {
    try {
        const { message, convoId } = response;
        console.log('Received message:', message);
        if (convoId === currentConversation.value.id) {
            chatMessages.value.push(message)
        }
    } catch (error) {
    console.error('Error parsing JSON:', error);
    }
    
})


</script>