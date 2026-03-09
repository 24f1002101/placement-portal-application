<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import { useAuthStore } from '@/stores/counter';
const auth_store = useAuthStore()
const auth_token = auth_store.getAuthToken()
const approved_companies = ref([])
async function fetchApprovedCompanies(){
    const response = await fetch("http://127.0.0.1:5000/api/display_all_approved_companies",{
        method : "GET",
        headers : {
            "Content-Type" : "application/json",
            "Authentication-Token" : auth_token
        }
    })
    if(response.ok){
        approved_companies.value = await response.json()
        console.log(approved_companies.value)
    }
}
onMounted(()=>{
    fetchApprovedCompanies();
})
</script>

<template>
<div class="container-fluid py-4 px-4 bg-light min-vh-100">
    <div class="row justify-content-center">
        <div class="col-12 col-lg-8">
            
            <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
                <div class="card-header bg-white border-bottom py-3">
                    <div class="d-flex align-items-center">
                        <div class="bg-primary bg-opacity-10 p-2 rounded-3 me-3">
                            <i class="bi bi-building text-primary"></i>
                        </div>
                        <h5 class="card-title mb-0 fw-bold text-dark">Approved Companies</h5>
                    </div>
                </div>

                <div class="card-body p-0">
                    <div v-if="approved_companies.length > 0" class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th class="ps-4 py-3 text-secondary small text-uppercase fw-bold">Company Name</th>
                                    <th class="pe-4 py-3 text-end text-secondary small text-uppercase fw-bold">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="company in approved_companies" :key="company.company_id">
                                    <td class="ps-4">
                                        <div class="d-flex align-items-center">
                                            <div class="avatar-sm me-3 bg-light rounded-circle d-flex align-items-center justify-content-center fw-bold text-primary border">
                                                {{ company.company_name.charAt(0).toUpperCase() }}
                                            </div>
                                            <span class="fw-medium text-dark">{{ company.company_name }}</span>
                                        </div>
                                    </td>
                                    <td class="pe-4 text-end">
                                        <RouterLink 
                                            :to="`/company/${company.company_id}/drives`" 
                                            class="btn btn-outline-primary btn-sm rounded-pill px-3 fw-500 transition-all"
                                        >
                                            View Drives
                                        </RouterLink>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div v-else class="text-center py-5 px-3">
                        <div class="mb-3">
                            <i class="bi bi-building-exclamation display-4 text-muted opacity-50"></i>
                        </div>
                        <h6 class="text-secondary fw-bold">No Companies Found</h6>
                        <p class="small text-muted mb-0">There are currently no approved companies to display.</p>
                    </div>
                </div>
            </div>

        </div>
    </div>
</div>
</template>

<style scoped>
/* Added minor visual polish that Bootstrap classes alone can't quite hit */
.avatar-sm {
    width: 32px;
    height: 32px;
    font-size: 0.8rem;
}

.transition-all {
    transition: all 0.2s ease-in-out;
}

.btn-outline-primary:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(13, 110, 253, 0.15);
}

.table thead th {
    letter-spacing: 0.03rem;
    font-size: 0.75rem;
}

.fw-500 {
    font-weight: 500;
}
</style>