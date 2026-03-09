<script setup>
import { useAuthStore } from '@/stores/counter';
import { ref, computed } from 'vue';
import router from '@/router';
import ongoing_drives from '@/components/ongoing_drives.vue';
import closed_drives from '@/components/closed_drives.vue';

const auth_store = useAuthStore();

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
    <div class="container py-4">

        <!-- Navbar -->
        <nav class="navbar navbar-dark bg-dark px-4 rounded mb-4">
            <span class="navbar-brand fw-bold">Company Dashboard</span>
            <div class="d-flex align-items-center gap-3" v-if="loginned">
                <span class="text-white">Welcome, <strong>{{ username }}</strong></span>
                <span class="badge" :class="{
                    'bg-success': status === 'approved',
                    'bg-warning text-dark': status === 'pending',
                    'bg-danger': status === 'blacklist'
                }">{{ status }}</span>
                <button class="btn btn-secondary btn-sm" @click="logouted">Logout</button>
            </div>
        </nav>

        <!-- Approved View -->
        <div v-if="status === 'approved'">

            <!-- Toggle Form Button -->
            <button class="btn btn-primary mb-3" @click="toggleDriveForm">
                {{ showDriveForm ? '✖ Close' : '➕ Create New Drive' }}
            </button>

            <!-- Drive Form -->
            <div v-if="showDriveForm" class="card p-4 mb-4 shadow-sm">
                <h5 class="fw-bold mb-3">New Job Drive Details</h5>
                <form @submit.prevent="handleCreateDrive">

                    <div class="mb-3">
                        <label class="form-label fw-semibold">Job Name</label>
                        <input v-model="driveData.name" type="text" class="form-control" required placeholder="Job Name" />
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-semibold">Description</label>
                        <textarea v-model="driveData.description" class="form-control" placeholder="Enter detailed job description"></textarea>
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-semibold">Deadline Date</label>
                        <input type="date" v-model="driveData.deadline_date" class="form-control" :min="minDate" @keydown.prevent required />
                        <small class="text-muted">Only current or future dates are allowed.</small>
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-semibold">Eligible Branches</label>
                        <input v-model="driveData.eligible_branch" type="text" class="form-control" placeholder="e.g CSE,ECE,EEE" />
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-semibold">Minimum CGPA</label>
                        <input v-model="driveData.cutoff_cgpa" type="number" step="0.01" class="form-control" placeholder="CGPA" />
                    </div>

                    <div class="mb-3">
                        <label class="form-label fw-semibold">Eligible Year</label>
                        <input v-model="driveData.eligibility_year" type="number" step="1" class="form-control" placeholder="Eligible Year" />
                    </div>

                    <button type="submit" class="btn btn-success w-100">Post Drive</button>
                </form>
            </div>

            <ongoing_drives :key="driveRefreshKey" @drive-closed="refresh"></ongoing_drives>
            <closed_drives :key="refreshKey"></closed_drives>
        </div>

        <!-- Restricted View -->
        <div v-else-if="status === 'pending' || status === 'blacklist'" class="text-center mt-5">
            <div class="alert alert-danger">
                <h5>Access Restricted</h5>
                <p>Your account status is currently <strong>{{ status }}</strong>.</p>
                <p>You cannot create drives until your account is approved by the admin.</p>
            </div>
        </div>

        <!-- Not Logged In -->
        <div v-else class="text-center mt-5">
            <div class="alert alert-warning">
                Please <RouterLink to="/">login</RouterLink> to access this page.
            </div>
        </div>

    </div>
</template>

<style scoped>
</style>