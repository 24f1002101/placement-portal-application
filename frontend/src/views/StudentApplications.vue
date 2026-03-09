<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useAuthStore } from '@/stores/counter';
import { useRoute} from 'vue-router';
const route = useRoute()
const auth_store = useAuthStore();
const user_email = auth_store.getUserEmail()
const auth_token = auth_store.getAuthToken()
const drive_id = route.params.drive_id
const applications = ref([])
async function fetch_applications(){
    const input = {
        drive_id : drive_id
    }
    const response = await fetch("http://127.0.0.1:5000/api/get_student_applications",{
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const output = await response.json()
        applications.value = output
    }
    else{
        alert(output.message)
        return
    }
}
onMounted(()=>{
    fetch_applications()
})
</script>

<template>
    <div class="container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="h4 fw-bold text-dark">Student Applications</h2>
            <RouterLink to="/company_dashboard" class="btn btn-outline-secondary btn-sm">
                <i class="bi bi-arrow-left"></i> Go Back
            </RouterLink>
        </div>

        <div v-if="applications.length > 0" class="card shadow-sm border-0">
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th class="ps-4">Student Name</th>
                            <th class="text-end pe-4">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="application in applications" :key="application.student_id">
                            <td class="ps-4 fw-medium">{{ application.student_name }}</td>
                            <td class="text-end pe-4">
                                <RouterLink 
                                    :to="`/review_application/${drive_id}/${application.student_id}`" 
                                    class="btn btn-primary btn-sm px-3"
                                >
                                    Review Application
                                </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div v-else class="alert alert-info border-0 shadow-sm rounded-3">
            <i class="bi bi-info-circle me-2"></i> No applications have been submitted for this drive yet.
        </div>
    </div>
</template>

<style scoped>
</style>