<template>
    <div>
        <b-card title="Card title" align="left">
            <div>
                <div class="card-columns m-4">
                    <UserProduct v-for="i in [1, 2, 3, 4, 5, 6]"></UserProduct>
                </div>
            </div>
        </b-card>
    </div>
</template>