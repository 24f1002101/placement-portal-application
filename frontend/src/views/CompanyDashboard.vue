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
// This function creates a YYYY-MM-DD string based on your LOCAL time
const getLocalToday = () => {
    const now = new Date();
    const offset = now.getTimezoneOffset() * 60000; // adjust for timezone
    const localISOTime = (new Date(now - offset)).toISOString().slice(0, 10);
    return localISOTime;
};

const minDate = getLocalToday(); // Used to disable past dates

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
    // Final safety check before submission
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
    console.log("Submitting Drive:", driveData.value);
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
    // Reset Form
    driveData.value = { 
        name: '', description: '', eligible_branch: '', 
        cutoff_cgpa: '', deadline_date: '' 
    };
};


</script>

<template>
    <div class="dashboard">
        <div class="header-bar">
            <div v-if="loginned">
                <span>Welcome, <strong>{{ username }}</strong></span>
                <span class="status-badge" :class="status">{{ status }}</span>
            </div>
            <button v-if="loginned" @click="logouted" class="logout-btn">Logout</button>
        </div>

        <div v-if="status === 'approved'" class="content">
            <button @click="toggleDriveForm" class="create-btn">
                {{ showDriveForm ? '✖ Close' : '➕ Create New Drive' }}
            </button>

            <div v-if="showDriveForm" class="form-container">
                <h3>New Job Drive Details</h3>
                <form @submit.prevent="handleCreateDrive">
                    <div class="field">
                        <label>Company/Drive Name</label>
                        <input v-model="driveData.name" type="text" required  placeholder="Job Name">
                    </div>

                    <div class="field">
                        <label>Description</label>
                        <textarea v-model="driveData.description" placeholder="enter detailed job description"></textarea>
                    </div>

                    <div class="field">
                        <label>Deadline Date</label>
                        <input 
                            type="date" 
                            v-model="driveData.deadline_date" 
                            :min="minDate" 
                            @keydown.prevent
                            required 
                        />
                        <p class="hint">Only current or future dates are allowed.</p>
                    </div>

                    <div class="field">
                        <label>Eligible Branches</label>
                        <input v-model="driveData.eligible_branch" type="text" placeholder="Branch e.g CSE/ECE/EEE"/>
                    </div>

                    <div class="field">
                        <label>Minimum CGPA</label>
                        <input v-model="driveData.cutoff_cgpa" type="number" step="0.01" placeholder="CGPA"/>
                    </div>

                    <div>
                        <label>Eligible Year</label>
                        <input v-model="driveData.eligibility_year" type="number" step="0.01" placeholder="eligible year"/>
                    </div>

                    <button type="submit" class="submit-btn">Post Drive</button>
                </form>
            </div>
            <ongoing_drives :key=driveRefreshKey @drive-closed="refresh"></ongoing_drives>
            <closed_drives :key=refreshKey></closed_drives>
        </div>

        <div v-else-if="status === 'pending' || status === 'blacklist'" class="restricted-view">
            <div class="error-card">
                <h2>Access Restricted</h2>
                <p>Your account status is currently <strong>{{ status }}</strong>.</p>
                <p>You cannot create drives until your account is approved by the admin.</p>
            </div>
        </div>

        <div v-else class="restricted-view">
            <p>Please <RouterLink to="/">login</RouterLink> to access this page.</p>
        </div>
    </div>
</template>

<style scoped>
.dashboard { padding: 30px; max-width: 900px; margin: auto; }
.header-bar { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #eee; padding-bottom: 15px; }
.status-badge { margin-left: 10px; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; text-transform: uppercase; }
.approved { background: #d4edda; color: #155724; }
.pending { background: #fff3cd; color: #856404; }
.blacklist { background: #f8d7da; color: #721c24; }

.create-btn { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 20px; }
.form-container { background: #f9f9f9; padding: 25px; border-radius: 8px; margin-top: 20px; border: 1px solid #ddd; }
.field { margin-bottom: 15px; }
.field label { display: block; margin-bottom: 5px; font-weight: bold; }
.hint { font-size: 0.8em; color: #666; margin-top: 4px; }

input, textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
.submit-btn { width: 100%; background: #28a745; color: white; border: none; padding: 12px; border-radius: 5px; cursor: pointer; font-size: 1.1em; }

.restricted-view { text-align: center; margin-top: 50px; }
.error-card { border: 1px solid #f5c6cb; background: #f8d7da; padding: 40px; border-radius: 10px; color: #721c24; }
.logout-btn { background: #6c757d; color: white; border: none; padding: 5px 15px; border-radius: 4px; cursor: pointer; }
</style>