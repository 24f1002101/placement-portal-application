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
    <div class="container mt-4">

        <!-- Approved Students -->
        <div class="mb-5">
            <h2 class="fw-bold fs-5 mb-3" v-if="!student_store.error_value">Registered Students</h2>

            <!-- IF SEARCHING -->
            <div v-if="searchType === 'student' && approvedlist.length">
                <table class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="student in approvedlist" :key="student.id">
                            <td>{{ student.name }}</td>
                            <td>
                                <button class="btn btn-danger btn-sm" @click="handleBlacklist(student.id)">Blacklist</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- ELSE NORMAL APPROVED LIST -->
            <div v-else>
                <div v-if="student_store.Approvedstudentslist.length === 0 && !student_store.error_value" class="alert alert-warning">
                    No Students Found !!!
                </div>
                <table v-else class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="student in student_store.Approvedstudentslist" :key="student.id">
                            <td>{{ student.name }}</td>
                            <td>
                                <button class="btn btn-danger btn-sm" @click="student_store.black_list(student.id)">Blacklist</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Pending Students -->
        <div>
            <h2 class="fw-bold fs-5 mb-3" v-if="!student_store.error_value">To be approved Students</h2>

            <!-- IF SEARCHING -->
            <div v-if="searchType === 'student' && pendinglist.length">
                <table class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="student in pendinglist" :key="student.id">
                            <td>{{ student.name }}</td>
                            <td>
                                <button class="btn btn-success btn-sm" @click="handleApprove(student.id)">Approve</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- ELSE NORMAL PENDING LIST -->
            <div v-else>
                <div v-if="student_store.Pendingstudents.length === 0 && !student_store.error_value" class="alert alert-warning">
                    No Students Found !!!
                </div>
                <table v-else class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="student in student_store.Pendingstudents" :key="student.id">
                            <td>{{ student.name }}</td>
                            <td>
                                <button class="btn btn-success btn-sm" @click="student_store.approve_Student(student.id)">Approve</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</template>