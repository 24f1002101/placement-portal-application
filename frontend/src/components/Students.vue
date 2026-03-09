<script setup>
import { ref, onMounted, computed } from 'vue';
import { studentStore } from '@/stores/student_store';

const emit = defineEmits(['action-taken'])
const student_store = studentStore()
const props = defineProps({
    searchResults: Array,
    searchType: String
})
const approvedlist = computed(() => {
    if (props.searchType !== 'student') return []
    return props.searchResults.filter(s => s.status === 'approved')
})
const pendinglist = computed(() => {
    if (props.searchType !== 'student') return []
    return props.searchResults.filter(s => s.status === 'pending')
})

async function handleBlacklist(studentId) {
    const success = await student_store.black_list(studentId)
    if (success) emit('action-taken', studentId)
}

async function handleApprove(studentId) {
    const success = await student_store.approve_Student(studentId)
    if (success) emit('action-taken', studentId)
}

onMounted(async () => {
    await student_store.fetchpendingstudents()
    await student_store.Approvedstudents()
})
</script>

<template>
    <div class="container-fluid py-4 px-4 bg-light min-vh-100">

        <div class="card shadow-sm border-0 mb-5">
            <div class="card-header bg-white border-bottom py-3 d-flex align-items-center justify-content-between">
                <h2 class="h5 mb-0 fw-bold text-dark" v-if="!student_store.error_value">
                    Registered Students
                </h2>
                <span class="badge rounded-pill bg-success-subtle text-success border border-success-subtle" v-if="searchType === 'student'">Search View</span>
            </div>
            
            <div class="card-body p-0">
                <div v-if="searchType === 'student' && approvedlist.length">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light text-secondary small text-uppercase">
                                <tr>
                                    <th class="ps-4">Student Name</th>
                                    <th class="text-end pe-4">Manage</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="student in approvedlist" :key="student.id">
                                    <td class="ps-4 fw-medium">{{ student.name }}</td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-outline-danger btn-sm px-3" @click="handleBlacklist(student.id)">Blacklist</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div v-else>
                    <div v-if="student_store.Approvedstudentslist.length === 0 && !student_store.error_value" class="p-5 text-center">
                        <p class="text-muted mb-0">No registered students found.</p>
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light text-secondary small text-uppercase">
                                <tr>
                                    <th class="ps-4">Student Name</th>
                                    <th class="text-end pe-4">Manage</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="student in student_store.Approvedstudentslist" :key="student.id">
                                    <td class="ps-4 fw-medium">{{ student.name }}</td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-outline-danger btn-sm px-3" @click="student_store.black_list(student.id)">Blacklist</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <div class="card shadow-sm border-0">
            <div class="card-header bg-white border-bottom py-3 d-flex align-items-center justify-content-between">
                <h2 class="h5 mb-0 fw-bold text-dark" v-if="!student_store.error_value">
                    To be approved Students
                </h2>
                <span class="badge rounded-pill bg-warning-subtle text-warning border border-warning-subtle" v-if="searchType === 'student'">Search View</span>
            </div>
            
            <div class="card-body p-0">
                <div v-if="searchType === 'student' && pendinglist.length">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light text-secondary small text-uppercase">
                                <tr>
                                    <th class="ps-4">Student Name</th>
                                    <th class="text-end pe-4">Review</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="student in pendinglist" :key="student.id">
                                    <td class="ps-4 fw-medium">{{ student.name }}</td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-success btn-sm px-4 shadow-sm" @click="handleApprove(student.id)">Approve</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div v-else>
                    <div v-if="student_store.Pendingstudents.length === 0 && !student_store.error_value" class="p-5 text-center">
                        <p class="text-muted mb-0">No pending approvals found.</p>
                    </div>
                    <div v-else class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead class="table-light text-secondary small text-uppercase">
                                <tr>
                                    <th class="ps-4">Student Name</th>
                                    <th class="text-end pe-4">Review</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="student in student_store.Pendingstudents" :key="student.id">
                                    <td class="ps-4 fw-medium">{{ student.name }}</td>
                                    <td class="text-end pe-4">
                                        <button class="btn btn-success btn-sm px-4 shadow-sm" @click="student_store.approve_Student(student.id)">Approve</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
/* Optional subtle styles to enhance the Bootstrap look */
.card {
    border-radius: 0.75rem;
    overflow: hidden;
}
.table thead th {
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    font-weight: 700;
}
.btn-sm {
    border-radius: 0.5rem;
    font-weight: 500;
}
</style>