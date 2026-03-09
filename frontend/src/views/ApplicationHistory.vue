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
    }
    else{
        const output = await response.json()
        alert(output.message)
    }
}
async function generate(student_id) {
    const auth_store = useAuthStore();
    const auth_token = auth_store.getAuthToken()
    const input = {
        student_id: student_id
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
    <div class="container-fluid py-4 px-4 bg-light min-vh-100">

        <nav class="navbar navbar-expand-lg navbar-white bg-white shadow-sm rounded-4 mb-4 px-3">
            <div class="container-fluid">
                <div class="d-flex align-items-center">
                    <div class="bg-primary bg-opacity-10 p-2 rounded-3 me-3">
                        <i class="bi bi-clock-history text-primary"></i>
                    </div>
                    <span class="navbar-brand mb-0 h1 fw-bold text-dark">Application History</span>
                </div>
                <div class="ms-auto d-flex gap-2">
                    <button 
                        v-if="applications.length > 0"
                        class="btn btn-success btn-sm px-3 rounded-pill d-flex align-items-center" 
                        @click="generate(student_id)"
                    >
                        <i class="bi bi-file-earmark-spreadsheet me-2"></i>Export CSV
                    </button>
                    <RouterLink to="/student_dashboard" class="btn btn-outline-secondary btn-sm px-3 rounded-pill">
                        <i class="bi bi-arrow-left me-1"></i>Back
                    </RouterLink>
                </div>
            </div>
        </nav>

        <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
            <div class="card-body p-0">
                <div v-if="applications.length > 0" class="table-responsive">
                    <table class="table table-hover align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th class="ps-4 py-3 text-secondary small text-uppercase fw-bold">App ID</th>
                                <th class="py-3 text-secondary small text-uppercase fw-bold">Company</th>
                                <th class="py-3 text-secondary small text-uppercase fw-bold">Job Role</th>
                                <th class="pe-4 py-3 text-end text-secondary small text-uppercase fw-bold">Current Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="application in applications" :key="application.application_id">
                                <td class="ps-4">
                                    <span class="text-muted fw-mono">#{{ application.application_id }}</span>
                                </td>
                                <td>
                                    <div class="fw-bold text-dark">{{ application.company_name }}</div>
                                </td>
                                <td>
                                    <span class="text-secondary small">{{ application.job_role }}</span>
                                </td>
                                <td class="pe-4 text-end">
                                    <span class="badge rounded-pill px-3 py-2"
                                        :class="{
                                            'bg-success-subtle text-success border border-success-subtle': application.status === 'selected',
                                            'bg-warning-subtle text-warning-emphasis border border-warning-subtle': application.status === 'waiting' || application.status === 'pending',
                                            'bg-danger-subtle text-danger border border-danger-subtle': application.status === 'rejected',
                                            'bg-info-subtle text-info-emphasis border border-info-subtle': application.status === 'shortlisted'
                                        }">
                                        <i class="bi bi-dot me-1"></i>
                                        {{ application.status.charAt(0).toUpperCase() + application.status.slice(1) }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-else class="p-5 text-center">
                    <div class="mb-3">
                        <i class="bi bi-folder2-open display-4 text-muted opacity-25"></i>
                    </div>
                    <h5 class="text-secondary fw-bold">No History Yet</h5>
                    <p class="text-muted small mx-auto" style="max-width: 300px;">
                        You haven't applied to any companies yet. Start your journey by exploring ongoing drives!
                    </p>
                    <RouterLink to="/student_dashboard" class="btn btn-primary btn-sm px-4 mt-2 rounded-pill">
                        Browse Drives
                    </RouterLink>
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
/* Aesthetic Polishing */
.fw-mono {
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.85rem;
}

.table thead th {
    font-size: 0.7rem;
    letter-spacing: 0.05rem;
}

.badge {
    font-weight: 600;
    font-size: 0.75rem;
    text-transform: capitalize;
}

/* Subtle row hover animation */
.table-hover tbody tr:hover {
    background-color: rgba(13, 110, 253, 0.02);
    transition: background-color 0.2s ease;
}

.card {
    transition: box-shadow 0.3s ease;
}
</style>