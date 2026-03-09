<script setup>
import { ref, onMounted } from 'vue';
import { companyStore } from '@/stores/company_store';
import { computed } from 'vue';

const emit = defineEmits(['action-taken'])
const company_store = companyStore()
const props = defineProps({
    searchResults: Array,
    searchType: String
})
const approved_list = computed(() => {
    if (props.searchType !== 'company') return []
    return props.searchResults.filter(c => c.status === 'approved')
})
const pending_companies = computed(() => {
    if (props.searchType !== 'company') return []
    return props.searchResults.filter(c => c.status === 'pending')
})

async function handleBlacklist(companyId) {
    const success = await company_store.black_list(companyId)
    if (success) emit('action-taken', companyId)
}

async function handleApprove(companyId) {
    const success = await company_store.approve_company(companyId)
    if (success) emit('action-taken', companyId)
}

onMounted(async () => {
    await company_store.fetchapprovedCompanies()
    await company_store.fetchpendingCompanies()
})
</script>

<template>
    <div class="container mt-4">

        <!-- Approved Companies -->
        <div class="mb-5">
            <h2 class="fw-bold fs-5 mb-3" v-if="!company_store.error_value">Registered Companies</h2>

            <!-- IF SEARCHING -->
            <div v-if="searchType === 'company' && approved_list.length">
                <table class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Company Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="company in approved_list" :key="company.company_id">
                            <td>{{ company.company_name }}</td>
                            <td>
                                <button class="btn btn-danger btn-sm" @click="handleBlacklist(company.company_id)">Blacklist</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- ELSE NORMAL APPROVED LIST -->
            <div v-else>
                <div v-if="company_store.approvedCompanies.length === 0 && !company_store.error_value" class="alert alert-warning">
                    No Companies Found !!!
                </div>
                <table v-else class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Company Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="company in company_store.approvedCompanies" :key="company.company_id">
                            <td>{{ company.company_name }}</td>
                            <td>
                                <button class="btn btn-danger btn-sm" @click="company_store.black_list(company.company_id)">Blacklist</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Pending Companies -->
        <div>
            <h2 class="fw-bold fs-5 mb-3" v-if="!company_store.error_value">To be approved Companies</h2>

            <!-- IF SEARCHING -->
            <div v-if="searchType === 'company' && pending_companies.length">
                <table class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Company Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="company in pending_companies" :key="company.company_id">
                            <td>{{ company.company_name }}</td>
                            <td>
                                <button class="btn btn-success btn-sm" @click="handleApprove(company.company_id)">Approve</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- ELSE NORMAL PENDING LIST -->
            <div v-else>
                <div v-if="company_store.pendingCompanies.length === 0 && !company_store.error_value" class="alert alert-warning">
                    No Companies Found !!!
                </div>
                <table v-else class="table table-bordered table-hover">
                    <thead class="table-dark">
                        <tr>
                            <th>Company Name</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="company in company_store.pendingCompanies" :key="company.company_id">
                            <td>{{ company.company_name }}</td>
                            <td>
                                <button class="btn btn-success btn-sm" @click="company_store.approve_company(company.company_id)">Approve</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</template>