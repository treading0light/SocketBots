<template>
    <div class="flex justify-end text-white">

        <LoginModal v-if="userLoggedIn === false" @login-ready="loginUser" />
        
        <ChatBox :chatMessages="chatMessages" @input-ready="sendInput" />

    </div>
</template>

<script setup>
import { io } from "socket.io-client"
const config = useRuntimeConfig()
console.log(`url  ${config.public.serverUrl}`)
const socket = io(config.public.serverUrl)

const userLoggedIn = ref(null)

const chatMessages = ref([])

const sendInput = (input) => {

    let message = { role: 'user', content: input }
    chatMessages.value.push(message)
    console.log(message)

    if (chatMessages.value.length >= 3) {
        let messages = JSON.stringify(chatMessages.value.slice(-3))
        
        socket.emit('user-input', messages)
    } else {
        let messages = JSON.stringify(chatMessages.value)
        socket.emit('user-input', messages)
    }
}

const loginUser = (credentials) => {
    socket.emit('login', credentials)
}

onMounted(() => {
    const jwtToken = useCookie('jwt')

    if (jwtToken) {
        userLoggedIn.value = true
    } else {
        userLoggedIn.value = false
    }
})

socket.on('connect', () => {
        console.log('Connected to server');
    })

socket.on('login-response', (response) => {
    if (response.status == 200) {
        userLoggedIn.value = true
    }
})

socket.on('ai-output', (response) => {
    let data = JSON.parse(response)
    console.log(data)
})

</script>