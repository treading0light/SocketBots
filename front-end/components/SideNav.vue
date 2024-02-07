<template>
    <div class="h-screen w-1/6 flex flex-col gap-2 bg-gray-400 p-2">
        <UButton @click="newConversation" label="New Conversation" color="primary" variant="outline"
        class="bg-primary text-black w-2/3 self-center" />
        <hr class="my-2">

        <div v-for="convo in conversations" :key="convo.id" class="flex">
            <UButton  @click="emit('conversationSelected', convo)" 
            class="text-black w-2/3 rounded-r-none">{{ convo.name >= 10 ? convo.name.substring(0, 10) : convo.name}}</UButton>

            <UButton  @click="deleteConversation(convo)" variant="outline"
            class="text-black bg-red-500 w-1/3 rounded-l-none">Delete</UButton>

        </div>

    </div>

</template>

<script setup>
const props = defineProps({
    socket: {
        type: Object,
        default: {}
    },
    currentConversation: {
        type: Object,
        default: {}
    },
    conversations: {
        type: Array,
        default: []
    }
})
const emit = defineEmits(['conversationSelected'])

const selectConversation = (conversation) => {
    props.currentConversation.value = conversation
}


const newConversation = () => {
    props.socket.emit('new-conversation', (response) => {
        console.log(`response from sidenav ${response.id}`)
        emit('conversationSelected', response)
    })
}

const deleteConversation = (conversation) => {
    props.socket.emit('delete-conversation', conversation.id, (response) => {
        console.log('deleted conversation')
        conversations.value = conversations.value.filter((convo) => convo.id !== conversation.id)
        console.log(response)
    })
}

props.socket.on('conversation-renamed', (response) => {
    const { name , id } = response
    let convo = conversations.value.find((c) => c.id === id)
    convo.name = name
    selectConversation(convo)
})

onMounted(() => {
    
})


</script>