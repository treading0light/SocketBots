<template>
    <div class="h-screen w-1/6 flex flex-col gap-2 bg-gray-400 p-2">
        <UButton @click="newConversation" label="New Conversation" color="primary"
        class=" text-black w-2/3 self-center" />
        <hr class="my-2">
        <div class="flex flex-col gap-2 overflow-y-auto">
            <div v-for="convo in conversations" :key="convo.id" class="flex justify-between">
                <UButton  @click="selectConversation(convo)"
                class="text-black w-2/3">{{ convo.name >= 10 ? convo.name.substring(0, 10) : convo.name}}</UButton>

                <UButton  @click="deleteConversation(convo)" variant="outline"
                class="text-black hover:bg-red-500 hover:text-white font-bold w-fit h-fit self-center justify-self-end">Delete</UButton>

            </div>
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
const emit = defineEmits(['conversation-selected', 'conversation-deleted'])

const selectConversation = (conversation) => {
    emit('conversation-selected', conversation.id)
}


const newConversation = () => {
    props.socket.emit('new-conversation', (response) => {
        console.log(`response from sidenav ${response.id}`)
        props.conversations.push(response)
        emit('conversation-selected', response)
    })
}

const deleteConversation = (conversation) => {
    props.socket.emit('delete-conversation', conversation.id, (response) => {
        console.log('deleted conversation')
        emit('conversation-deleted', conversation)
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
    setTimeout(() => {
        if (props.conversations.length > 0) {
            selectConversation(props.conversations[0])
            console.log('selected conversation' + props.conversations[0])
        }
    }, 100);
    
})


</script>