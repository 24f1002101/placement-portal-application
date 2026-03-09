<script setup>
import { useAuthStore } from '@/stores/counter';
import { ref } from 'vue';
import { onMounted } from 'vue';
import { defineEmits } from 'vue';
const auth_store = useAuthStore();
const emit = defineEmits(['drive-closed'])
const ongoing_companies = ref([])
async function ongoing_drives(){
    const auth_token = auth_store.getAuthToken()
    const mail = auth_store.getUserEmail()
    const input = {
        email : mail
    }
    const response = await fetch("http://127.0.0.1:5000/api/ongoing_drives",{
        method : "POST",
        headers:
            {  
                "Content-Type" : "application/json",
                "Authentication-Token" : auth_token
            },
        body : JSON.stringify(input)
    })
    if(!response.ok){
        const output = await response.json()
        alert(output.message)
    }
    else{
        ongoing_companies.value = await response.json()
    }
}
async function close_drive(placement_id){
    const auth_token = auth_store.getAuthToken()
    const mail = auth_store.getUserEmail()
    const input = {
        id : placement_id
    }
    const response = await fetch("http://127.0.0.1:5000/api/close_drive",{
        method : "PUT",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(input)
    })
    if(response.ok){
        const output = await response.json()
        alert(output.message)
        emit('drive-closed')
    }
    await ongoing_drives()
}
onMounted(()=>{
    ongoing_drives()
})
</script>

<template>
    <div class="container-fluid py-4">
        <div class="card shadow-sm border-0">
            <div class="card-header bg-white py-3">
                <h5 class="mb-0 fw-bold text-primary">
                    <i class="bi bi-briefcase-fill me-2"></i>Ongoing Placement Drives
                </h5>
            </div>

            <div class="card-body p-0">
                <div v-if="ongoing_companies.length > 0" class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light text-secondary small text-uppercase">
                            <tr>
                                <th class="px-4">Drive ID</th>
                                <th>Company</th>
                                <th>Role</th>
                                <th>Description</th>
                                <th>Year</th>
                                <th>Branch</th>
                                <th>Min CGPA</th>
                                <th class="text-end px-4">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="drive in ongoing_companies" :key="drive.id">
                                <td class="px-4 text-muted">#{{ drive.id }}</td>
                                <td>
                                    <span class="fw-bold text-dark">{{ drive.company_details.company_name }}</span>
                                </td>
                                <td><span class="badge bg-info-subtle text-info border border-info-subtle rounded-pill px-3">{{ drive.job_title }}</span></td>
                                <td class="text-truncate" style="max-width: 200px;">{{ drive.job_description }}</td>
                                <td>{{ drive.eligibility_year }}</td>
                                <td>{{ drive.eligibility_branch }}</td>
                                <td><span class="fw-medium text-success">{{ drive.eligibility_cgpa }}</span></td>
                                <td class="text-end px-4">
                                    <div class="btn-group shadow-sm">
                                        <RouterLink :to="`/get_applications/${drive.id}`" class="btn btn-outline-primary btn-sm">
                                            View Details
                                        </RouterLink>
                                        <button @click="close_drive(drive.id)" class="btn btn-success btn-sm">
                                            Mark Complete
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-else class="p-5 text-center">
                    <div class="display-6 text-muted mb-3"><i class="bi bi-folder2-open"></i></div>
                    <p class="h5 text-secondary">No Ongoing Drives Found</p>
                    <p class="small text-muted">You haven't initiated any placement drives yet.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Minor cleanup for table text fluidity */
.table-responsive {
    scrollbar-width: thin;
}
.btn-sm {
    font-size: 0.75rem;
    padding: 0.4rem 0.8rem;
}
</style>