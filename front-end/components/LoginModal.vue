<template>
    <UModal prevent-close class="flex flex-col items-center gap-10">
        <h1>Who's there?</h1>

        <UInput v-model="email" color="primary" variant="outline" placeholder="Email..." />

        <UInput v-model="password" color="primary" variant="outline" placeholder="Password" />

        <UButton @click="submitLogin" label="Submit" color="primary" variant="outline" />
    </UModal>
</template>

<script setup>
const email = ref('')
const password = ref('')

const emit = defineEmits(['login-sucess'])

const submitLogin = async () => {
    const config = useRuntimeConfig()
    const { data, error } = await useFetch(`${config.public.serverUrl}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email.value, password: password.value }),
    })

    if (error) {
        console.error(error)
    } else {
        console.log(data)
        emit('login-sucess')
    }
}
</script>