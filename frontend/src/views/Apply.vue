<script setup>
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import router from '@/router'

const route = useRoute()
const auth_store = useAuthStore()
const auth_token = auth_store.getAuthToken()
const resume = ref(null)
const placement_id = route.params.placement_id
const company_id = route.params.company_id
const email = auth_store.getUserEmail()


function handleFileChange(event) {
     const file = event.target.files[0]
    
    if (!file) return

    if (file.type !== 'application/pdf') {
        alert('Please upload a PDF file only.')
        event.target.value = ''
        resume.value = null
        return
    }

    resume.value = file
}
async function applyDrive(id){
    if(!resume.value){
        alert("Please select your resume in a PDF format first !!!")
        return 
    }
    const form_data = new FormData()
    form_data.append('resume',resume.value)
    form_data.append('placement_id',id)
    form_data.append('email',email)
    const response = await fetch("http://127.0.0.1:5000/api/apply_drive",{
        method : "POST",
        headers :{
            'Authentication-Token' : auth_token
        },
        body : form_data
    })
    if(response.ok){
        const output = await response.json()
        alert(output.message)
    }
    else{
        const output = await response.json()
        alert(output.message)
    }

}
</script>

<template>
    <div>
        <input type="file" accept=".pdf" @change="handleFileChange" />
        <button @click="applyDrive(placement_id)">Apply</button>
        <RouterLink :to="`/company/${company_id}/drives`"><button>Go Back</button></RouterLink>
    </div>
</template>

<style scoped>
</style>