<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useAuthStore } from '@/stores/counter';
import { useRoute } from 'vue-router';
import router from '@/router';
const route = useRoute()
const drive_id = route.params.drive_id
const student_id = route.params.student_id
const auth_store = useAuthStore()
async function view_resume(){
    const auth_token = auth_store.getAuthToken()
    const input = {
        drive_id : drive_id,
        student_id : student_id
    }
    const response = await fetch("http://127.0.0.1:5000/api/view_resume",{
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        window.open(url,'_blank')
        router.push('/student_applications')
    }
    else{
        const output = await response.json()
        alert(output.message)
    }
}
onMounted(()=>{
    view_resume()
})
</script>

<template>
    <div>
    </div>
</template>

<style scoped>
</style>