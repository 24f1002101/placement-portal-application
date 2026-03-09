<script setup>
import { useAuthStore } from '@/stores/counter';
import { ref } from 'vue';
import { onMounted } from 'vue';
const auth_store = useAuthStore();
const closed_companies = ref([])
async function closed_drives(){
    const auth_token = auth_store.getAuthToken()
    const mail = auth_store.getUserEmail()
    const input = {
        email : mail
    }
    const response = await fetch("http://127.0.0.1:5000/api/closed_drives",{
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
        closed_companies.value = await response.json()
    }
}
onMounted(()=>{
    closed_drives()
})
</script>

<template>
    <div class="container-fluid py-4 px-4">
        <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-bottom py-3 d-flex align-items-center">
                <div class="bg-secondary bg-opacity-10 p-2 rounded me-3">
                    <i class="bi bi-archive-fill text-secondary"></i>
                </div>
                <h2 class="h5 mb-0 fw-bold text-dark">Closed Placement Drives</h2>
            </div>
            
            <div class="card-body p-0">
                <div v-if="closed_companies.length > 0" class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light text-secondary small text-uppercase">
                            <tr>
                                <th class="ps-4">ID</th>
                                <th>Company Name</th>
                                <th>Role</th>
                                <th>Description</th>
                                <th>Year</th>
                                <th>Branch</th>
                                <th class="pe-4">Min. CGPA</th>
                            </tr>
                        </thead>
                        <tbody class="text-dark">
                            <tr v-for="drive in closed_companies" :key="drive.id">
                                <td class="ps-4">
                                    <span class="badge bg-light text-secondary border">#{{ drive.id }}</span>
                                </td>
                                <td class="fw-bold">{{ drive.company_details.company_name }}</td>
                                <td>
                                    <span class="badge bg-secondary-subtle text-secondary rounded-pill px-3">
                                        {{ drive.job_title }}
                                    </span>
                                </td>
                                <td class="text-muted small" style="max-width: 250px;">
                                    {{ drive.job_description }}
                                </td>
                                <td>{{ drive.eligibility_year }}</td>
                                <td>{{ drive.eligibility_branch }}</td>
                                <td class="pe-4">
                                    <span class="fw-medium">{{ drive.eligibility_cgpa }}</span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-else class="p-5 text-center">
                    <div class="mb-3 text-muted opacity-50">
                        <i class="bi bi-folder-x display-4"></i>
                    </div>
                    <p class="h6 text-secondary fw-normal">No Closed Drives Found</p>
                    <p class="small text-muted mb-0">Once a drive is completed, it will appear here in your archives.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Scoped adjustments to handle text overflow and spacing */
.table th {
    font-size: 0.75rem;
    letter-spacing: 0.05rem;
    font-weight: 700;
}

.table td {
    font-size: 0.9rem;
    padding-top: 1rem;
    padding-bottom: 1rem;
}

.card {
    border-radius: 0.75rem;
    overflow: hidden;
}
</style>