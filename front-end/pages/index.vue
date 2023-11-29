<template>
    <div class="flex justify-end">

        <LoginModal v-if="userLoggedIn === false" @login-ready="loginUser" />
        
        <ChatBox :chatMessages="chatMessages" />

    </div>
</template>

<script setup>
import { io } from "socket.io-client"
const config = useRuntimeConfig()
const socket = io(config.public.serverUrl)

const userLoggedIn = ref(null)

const inputText = ref('')
const chatMessages = ref([])

const sendInput = (event) => {
    event.preventDefault()

    let message = { role: 'user', content: inputText.value }
    chatMessages.value.push(message)

    inputText.value = ''
    console.log(chatMessages.value)
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

</script>