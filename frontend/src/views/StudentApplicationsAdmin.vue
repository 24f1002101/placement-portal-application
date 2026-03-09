<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/counter';
const auth_store = useAuthStore()
import { onMounted } from 'vue';
const applications = ref([])

async function fetch_applications(){
    const auth_token = auth_store.getAuthToken()
    const response = await fetch("http://127.0.0.1:5000/api/get_all_applications",{
        method : "GET",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        }
    })
    if(response.ok){
        const output = await response.json()
        applications.value = output
    }
}
onMounted(()=>{
    fetch_applications()
})

</script>

<template>
    <div>
        <div v-if="applications.length > 0">
            <table border="1">
                <thead>
                    <th>Application ID</th>
                    <th>Dive ID</th>
                    <th>Student Name</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                    <th>Year</th>
                    <th>Company Name</th>
                    <th>Application Date</th>
                    <th>Application Status</th>
                    <th>Action</th>
                </thead>
                <tbody>
                    <tr v-for="application in applications" :key="application.application_id">
                        <td>{{ application.application_id }}</td>
                        <td>{{ application.drive_id }}</td>
                        <td>{{ application.student_name }}</td>
                        <td>{{ application.branch }}</td>
                        <td>{{ application.cgpa }}</td>
                        <td>{{ application.year }}</td>
                        <td>{{ application.company_name }}</td>
                        <td>{{ application.application_date }}</td> 
                        <td>{{ application.status }}</td> 
                        <td><RouterLink :to="`/view/${application.student_id}/${application.drive_id}`"><button>View</button></RouterLink></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            No Student Applications !!!
        </div>
        <div>
            <RouterLink to="/admin_dashboard">Go Back</RouterLink>
        </div>
    </div>
</template>

<style scoped>

</style>