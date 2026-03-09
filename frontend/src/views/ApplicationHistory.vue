<script setup>
import { useAuthStore } from '@/stores/counter';
import { ref } from 'vue';
import { onMounted } from 'vue';
const applications = ref([])
const student_id = ref(0)
async function history(){
    const auth_store = useAuthStore();
    const email = auth_store.getUserEmail()
    const auth_token = auth_store.getAuthToken()
    const input = {
        email  : email
    }
    const response = await fetch("http://127.0.0.1:5000/api/get_history",{
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)

    })
    if(response.ok){
        const output = await response.json()
        applications.value = output.history
        student_id.value = output.student_id
        console.log(applications.value)
        console.log(student_id.value)
    }
    else{
        const output = await response.json()
        alert(output.message)
    }
}
async function generate(student_id) {
    const auth_store = useAuthStore();
    const email = auth_store.getUserEmail()
    const auth_token = auth_store.getAuthToken()
    const input = {
        student_id :student_id
    }
    const response = await fetch("http://127.0.0.1:5000/api/get_csv",{
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
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
onMounted(()=>{
    history()
})
</script>

<template>
    <div>
        <div v-if="applications.length>0">
            <table border="1">
                <thead>
                    <th>Application ID</th>
                    <th>Company Name</th>
                    <th>Job Role</th>
                    <th>Status</th>
                </thead>
                <tbody>
                    <tr v-for="application in applications" :key="application.id">
                        <td>{{ application.application_id }}</td>
                        <td>{{ application.company_name }}</td>
                        <td>{{ application.job_role }}</td>
                        <td>{{ application.status }}</td>
                    </tr>
                </tbody>
            </table>
            <button v-on:click="generate(student_id)">Generate CSV</button>
        </div>
        <div v-else>
            No Application History Found !!!
        </div>
        <div>
            <RouterLink to="/student_dashboard"><button>Go Back</button></RouterLink>
        </div>
    </div>
</template>

<style scoped>
</style>