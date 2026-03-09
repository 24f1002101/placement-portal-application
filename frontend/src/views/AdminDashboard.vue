<script setup>
import { useAuthStore } from '@/stores/counter';
import { onMounted, ref } from 'vue';
import router from '@/router';
import Companies from '@/components/Companies.vue';
import Students from '@/components/Students.vue';
const auth_store = useAuthStore()
const search_value = ref('')
console.log(auth_store.isAuthenticated)
const username = ref(JSON.parse(localStorage.getItem('user'))?.name || null)
const searchType = ref('student')
const searchResults = ref([])
async function handleSearch(){
    const response = await fetch(`http://127.0.0.1:5000/api/admin_search?type=${searchType.value}&query=${search_value.value}`,{
        method : 'GET',
        headers: {
            "Authentication-Token" : auth_store.getAuthToken()
        }
    })
    if(response.ok){
        searchResults.value = await response.json()
    }
}
console.log(username)
function logouting(){
    auth_store.clearAuthToken()
    alert("Logouted Successfully !!!")
    router.push('/')
}
function removeFromSearch(id) {
    searchResults.value = searchResults.value.filter(item => 
        (item.id !== id && item.company_id !== id)
    );
}
</script>

<template>
    <div v-if="username" class="min-vh-100 bg-light">

        <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm sticky-top mb-4">
            <div class="container-fluid px-4">
                <a class="navbar-brand fw-bold text-primary" href="#">
                    <i class="bi bi-shield-lock-fill me-2"></i>Admin Panel
                </a>
                
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-3">
                        <li class="nav-item">
                            <RouterLink to="/ongoing_drives_admin" class="nav-link px-3">
                                <i class="bi bi-activity me-1"></i>Ongoing Drives
                            </RouterLink>
                        </li>
                        <li class="nav-item">
                            <RouterLink to="/student_applications" class="nav-link px-3">
                                <i class="bi bi-file-earmark-text me-1"></i>Applications
                            </RouterLink>
                        </li>
                    </ul>
                    
                    <div class="d-flex align-items-center gap-3">
                        <div class="text-end d-none d-sm-block">
                            <small class="text-muted d-block">Welcome back,</small>
                            <span class="fw-bold text-dark">{{ username }}</span>
                        </div>
                        <div class="vr mx-2 d-none d-sm-block"></div>
                        <button class="btn btn-outline-danger btn-sm px-3 rounded-pill" @click="logouting">
                            <i class="bi bi-box-arrow-right me-1"></i>Logout
                        </button>
                    </div>
                </div>
            </div>
        </nav>

        <div class="container mb-5">
            <div class="card border-0 shadow-sm p-4 rounded-4">
                <div class="row g-3 align-items-end">
                    <div class="col-md-5">
                        <label class="form-label small fw-bold text-secondary">Find Records</label>
                        <div class="input-group">
                            <span class="input-group-text bg-white border-end-0"><i class="bi bi-search text-muted"></i></span>
                            <input class="form-control border-start-0" v-model="search_value" placeholder="Type name or ID..." @keyup.enter="handleSearch" />
                        </div>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label small fw-bold text-secondary">Category</label>
                        <select class="form-select" v-model="searchType">
                            <option value="student">Students Directory</option>
                            <option value="company">Company Partners</option>
                        </select>
                    </div>
                    <div class="col-md-2">
                        <button class="btn btn-primary w-100 fw-bold" @click="handleSearch">
                            Search
                        </button>
                    </div>
                    <div class="col-md-2" v-if="searchResults.length">
                        <button class="btn btn-light w-100 text-secondary" @click="searchResults = []">
                            Clear
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div class="container pb-5">
            <div class="row">
                <div class="col-12">
                    <Companies 
                        :searchResults="searchResults" 
                        :searchType="searchType" 
                        @action-taken="removeFromSearch"
                    ></Companies>
                    
                    <div class="my-4"></div> <Students 
                        :searchResults="searchResults" 
                        :searchType="searchType" 
                        @action-taken="removeFromSearch"
                    ></Students>
                </div>
            </div>
        </div>

    </div>

    <div v-else class="min-vh-100 d-flex align-items-center bg-light">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-5">
                    <div class="card border-0 shadow-lg text-center p-5 rounded-4">
                        <div class="mb-4">
                            <i class="bi bi-exclamation-triangle text-warning display-1"></i>
                        </div>
                        <h3 class="fw-bold">Access Denied</h3>
                        <p class="text-muted">You must be logged in as an administrator to access this dashboard.</p>
                        <RouterLink to="/" class="btn btn-primary px-5 rounded-pill mt-3">Go to Login</RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Scoped styles to polish the Bootstrap experience */
.navbar-brand {
    letter-spacing: -0.5px;
}

.nav-link {
    font-weight: 500;
    color: #6c757d;
    transition: color 0.2s;
}

.nav-link:hover {
    color: #0d6efd;
}

.form-control:focus, .form-select:focus {
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
    border-color: #0d6efd;
}

.card {
    transition: transform 0.2s ease;
}

/* Custom separator for the vertical rule */
.vr {
    width: 1px;
    background-color: #dee2e6;
    height: 30px;
}
</style>