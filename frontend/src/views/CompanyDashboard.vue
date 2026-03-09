<script setup>
import { useAuthStore } from '@/stores/counter';
import { ref, computed } from 'vue';
import router from '@/router';
import ongoing_drives from '@/components/ongoing_drives.vue';
import closed_drives from '@/components/closed_drives.vue';

const auth_store = useAuthStore();

// 1. Reactive Auth & User Data
const loginned = computed(() => auth_store.isAuthenticated);
const driveRefreshKey = ref(0);
const refreshKey = ref(0);
const userData = computed(() => {
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
});
const username = computed(() => userData.value?.name || 'User');
const status = computed(() => userData.value?.status || '');
const mail = computed(()=> userData.value?.email || '');
const password = computed(()=> userData.value?.password || '');
const auth_token = auth_store.getAuthToken()
const company_id = ref('')
// 2. FOOLPROOF DATE RESTRICTION
const getLocalToday = () => {
    const now = new Date();
    const offset = now.getTimezoneOffset() * 60000; 
    const localISOTime = (new Date(now - offset)).toISOString().slice(0, 10);
    return localISOTime;
};

const minDate = getLocalToday(); 

function refresh(){
    refreshKey.value++
}
// 3. Form State
const showDriveForm = ref(false);
const driveData = ref({
    name: '',
    description: '',
    eligible_branch: '',
    cutoff_cgpa: '',
    deadline_date: '',
    eligibility_year :''
});

function toggleDriveForm() {
    showDriveForm.value = !showDriveForm.value;
};

function logouted() {
    auth_store.clearAuthToken();
    alert("Successfully logged out!");
    router.push("/");
};

async function handleCreateDrive() {
    if (driveData.value.deadline_date < minDate) {
        alert("Error: You cannot select a date in the past!");
        return;
    }
    if(driveData.value.cutoff_cgpa > 10 || driveData.cutoff_cgpa < 5){
        alert("Error : Check cgpa , cgpa must be lesser than or equal to 10 !!!");
        return;
    }
    if(driveData.value.eligibility_year > 4 || driveData.eligibility_year < 1){
        alert("Error : Enter year between 1 to 4 !!!")
        return;
    }
    
    const data = {
        eligible_year : driveData.value.eligibility_year,
        eligible_branch : driveData.value.eligible_branch,
        cutoff_cgpa : driveData.value.cutoff_cgpa,
        email : mail.value,
        application_deadline : driveData.value.deadline_date,
        job_role : driveData.value.name,
        job_description : driveData.value.description
    }
    const response = await fetch("http://127.0.0.1:5000/api/create_drive",{
        method : "POST",
        headers :{
            "Content-Type": "application/json",
            "Authentication-Token" : auth_token
        },
        body : JSON.stringify(data)
    })
    if(response.ok){
        const output = await response.json()
        alert("Drive Created Successfully !!!");
        driveRefreshKey.value++;
    }
   
    showDriveForm.value = false;
    driveData.value = { 
        name: '', description: '', eligible_branch: '', 
        cutoff_cgpa: '', deadline_date: '' 
    };
};
</script>

<template>
    <div class="min-vh-100 bg-light">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm mb-4">
            <div class="container">
                <span class="navbar-brand fw-bold">Company Dashboard</span>
                
                <div class="ms-auto d-flex align-items-center gap-3">
                    <div v-if="loginned" class="d-flex align-items-center text-white me-2">
                        <span class="small me-2">Welcome, <strong>{{ username }}</strong></span>
                        <span class="badge rounded-pill" 
                            :class="{
                                'bg-success': status === 'approved',
                                'bg-warning text-dark': status === 'pending',
                                'bg-danger': status === 'blacklist'
                            }">
                            {{ status }}
                        </span>
                    </div>
                    <button v-if="loginned" @click="logouted" class="btn btn-outline-light btn-sm rounded-pill px-3">
                        Logout
                    </button>
                </div>
            </div>
        </nav>

        <div class="container pb-5">
            <div v-if="status === 'approved'">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <h2 class="h4 fw-bold text-dark mb-0">Recruitment Management</h2>
                    <button @click="toggleDriveForm" class="btn shadow-sm fw-bold px-4" 
                        :class="showDriveForm ? 'btn-secondary' : 'btn-primary'">
                        {{ showDriveForm ? '✖ Cancel' : '➕ Create New Drive' }}
                    </button>
                </div>

                <div v-if="showDriveForm" class="card border-0 shadow-sm mb-5 rounded-4 overflow-hidden">
                    <div class="card-header bg-primary text-white py-3">
                        <h5 class="mb-0 fw-bold">Post a New Job Opening</h5>
                    </div>
                    <div class="card-body p-4 bg-white">
                        <form @submit.prevent="handleCreateDrive" class="row g-3">
                            <div class="col-md-6">
                                <label class="form-label fw-bold small">Job Role / Drive Name</label>
                                <input v-model="driveData.name" type="text" class="form-control px-3 py-2" required placeholder="e.g. Software Engineer">
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-bold small">Deadline Date</label>
                                <input type="date" v-model="driveData.deadline_date" class="form-control px-3 py-2" :min="minDate" @keydown.prevent required />
                                <div class="form-text text-muted small">Only current or future dates.</div>
                            </div>

                            <div class="col-12">
                                <label class="form-label fw-bold small">Job Description</label>
                                <textarea v-model="driveData.description" class="form-control px-3 py-2" rows="3" placeholder="Describe the responsibilities and skills required..."></textarea>
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-bold small">Eligible Branches</label>
                                <input v-model="driveData.eligible_branch" type="text" class="form-control px-3 py-2" placeholder="e.g. CSE/ECE">
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-bold small">Minimum CGPA</label>
                                <input v-model="driveData.cutoff_cgpa" type="number" step="0.01" class="form-control px-3 py-2" placeholder="e.g. 7.5">
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-bold small">Eligible Year</label>
                                <input v-model="driveData.eligibility_year" type="number" step="0.01" class="form-control px-3 py-2" placeholder="e.g. 4">
                            </div>

                            <div class="col-12 mt-4 text-end">
                                <button type="submit" class="btn btn-success btn-lg px-5 shadow-sm rounded-pill fw-bold">
                                    Launch Drive
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <div class="row">
                    <div class="col-12">
                        <ongoing_drives :key="driveRefreshKey" @drive-closed="refresh"></ongoing_drives>
                        <div class="my-5 border-top opacity-25"></div>
                        <closed_drives :key="refreshKey"></closed_drives>
                    </div>
                </div>
            </div>

            <div v-else-if="status === 'pending' || status === 'blacklist'" class="row justify-content-center py-5">
                <div class="col-md-6 text-center">
                    <div class="card border-0 shadow-lg rounded-4 p-5">
                        <div class="mb-4 text-danger">
                            <i class="bi bi-shield-slash-fill display-1"></i>
                        </div>
                        <h2 class="fw-bold text-dark">Access Restricted</h2>
                        <p class="text-muted lead">Your current account status is 
                            <span class="badge" :class="status === 'blacklist' ? 'bg-danger' : 'bg-warning text-dark'">{{ status }}</span>
                        </p>
                        <hr class="my-4 mx-auto w-50">
                        <p class="text-secondary">Please wait for the administrator to review and approve your profile before you can create placement drives.</p>
                    </div>
                </div>
            </div>

            <div v-else class="row justify-content-center py-5">
                <div class="col-md-4 text-center">
                    <div class="alert alert-info shadow-sm rounded-4 py-4 px-4 border-0">
                        <p class="mb-3 fw-medium">Authentication Required</p>
                        <RouterLink to="/" class="btn btn-primary px-4 rounded-pill">Proceed to Login</RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Minor aesthetic refinements to extend Bootstrap */
.form-control:focus {
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
}

.card {
    transition: transform 0.2s ease;
}

label {
    letter-spacing: 0.02rem;
    color: #495057;
}

.btn-lg {
    font-size: 1rem;
}
</style>