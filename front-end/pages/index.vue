<template>
    <div class="flex justify-end">
        <SideNav @request-rename="requestRename" @conversationDeleted="removeConversation" @conversation-selected="selectConversation"
        :conversations="conversations" :currentConversation="currentConversation" :socket="socket" />

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

const sendInput = (input) => {

    let userMessage = { role: 'user', content: input, conversation_id: currentConversation.value.id }

    let messages = []
    if (currentConversation.value.messages.length >= 20) {
        messages = currentConversation.value.messages.slice(-20)
    } else {
        messages = currentConversation.value.messages
    }

    const req = { messages: messages, user_message: userMessage, conversation_id: currentConversation.value.id }

    socket.emit('user-input', req, (response) => {
        console.log('response from server' + typeof(response) + response)
        currentConversation.value.messages.push(response)
    })
}

const removeConversation = (conversation) => {
    conversations.value = conversations.value.filter((convo) => convo.id !== conversation.id)
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

const cleanMessage = (message) => {
    return { content: message.content, role: message.role }
}

onMounted(() => {
    getAllConversations()
})

socket.on('connect', () => {
        console.log('Connected to server');
    })

socket.on('ai-output', (response) => {
    try {
        const message = response;
        console.log('Received message:', message);
        currentConversation.value.messages.push(cleanMessage(message))
    } catch (error) {
    console.error('Error parsing JSON:', error);
    }
    
})


</script>