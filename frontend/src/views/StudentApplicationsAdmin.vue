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
    <div class="container mt-4">

        <div v-if="applications.length > 0">
            <table class="table table-bordered table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Application ID</th>
                        <th>Drive ID</th>
                        <th>Student Name</th>
                        <th>Branch</th>
                        <th>CGPA</th>
                        <th>Year</th>
                        <th>Company Name</th>
                        <th>Application Date</th>
                        <th>Application Status</th>
                        <th>Action</th>
                    </tr>
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
                        <td>
                            <RouterLink :to="`/view/${application.student_id}/${application.drive_id}`">
                                <button class="btn btn-primary btn-sm">View</button>
                            </RouterLink>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-else class="alert alert-warning">
            No Student Applications !!!
        </div>

        <RouterLink to="/admin_dashboard" class="btn btn-secondary mt-2">Go Back</RouterLink>

    </div>
</template>

<style scoped>
</style>