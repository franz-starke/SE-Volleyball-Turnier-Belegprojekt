<script setup>
import QrcodeVue, { QrcodeCanvas, QrcodeSvg } from "qrcode.vue";
import { QrcodeStream, QrcodeDropZone, QrcodeCapture } from "vue-qrcode-reader";
import { ref, onMounted, watch } from "vue";
import { useTournamentStore } from "@/stores/tournamentStore";
import IconQrCode from "../icons/IconQrCode.vue";
import IconTrophy from "../icons/IconTrophy.vue";
import { gzip, ungzip } from "pako";
import { evaluateTournamentData } from "@/util/tournamentEvaluation.js";
import IconCamera from "../icons/IconCamera.vue";

const store = useTournamentStore();

const syncGames = ref(false);
const evalShow = ref(false);
const qrSize = ref(0);
onMounted(() => {
	const minSize = Math.min(window.innerWidth, window.innerHeight);
	qrSize.value = minSize <= 750 ? minSize * 0.85 : 750;
});

// QrCode data for offline sync
// 1. Convert to JSON string
// qr code can hold max of 1273 characters at Level H and 2953 at Level L
const jsonStr = JSON.stringify(store.tournament);
console.log("Tournament JSON String: ", jsonStr, "Length: ", jsonStr.length);
// 2. Compress using GZIP
const compressed = gzip(jsonStr);
console.log(
	"Compressed:",
	compressed,
	"Compressed Length: ",
	compressed.length
);
// 3. Encode to Base64 (QR-safe string)
const base64Encoded = btoa(String.fromCharCode(...compressed));
console.log("Base64 Encoded:", base64Encoded, "Length: ", base64Encoded.length);
const qrvalue = ref(base64Encoded); // this works, because the longest possible Tournament Json String results to 2756 characters,which is in the Limits of an L level QR Code

// Qr scanner function
function onDetect(detectedCodes) {
	// detectedCodes is a Proxy Array
	const rawValue = detectedCodes[0].rawValue;
	if (rawValue === "") {
		alert("Bitte scannen Sie einen gültigen QR-Code.");
		return;
	}
	const decoded = atob(rawValue);
	const decompressed = ungzip(
		new Uint8Array([...decoded].map((c) => c.charCodeAt(0))),
		{ to: "string" }
	);

	// Parse the JSON string back to an object
	const tournamentData = JSON.parse(decompressed);

	// Update the store with the new tournament data
	store.tournament = tournamentData;

	console.log("Tournament data updated:", tournamentData);
}

function toggleSyncGames() {
	syncGames.value = !syncGames.value;
}

const leaderboard = ref({});
function evalTournament() {
	console.log("Evaluating Tournament...");
	leaderboard.value = evaluateTournamentData(store.tournament);
	console.log("Leaderboard: ", leaderboard);
	evalShow.value = true;
}

const activeGroup = ref(0);
function setActiveGroup(groupIndex) {
	activeGroup.value = groupIndex;
}
</script>

<template>
	<div class="h-full overflow-y-auto scrollbar-hidden">
		<div v-if="evalShow" id="eval-dialog" class="flex flex-col flex-1">
			<div class="sticky top-0 z-10 bg-[var(--color-background)] pb-2">
				<div class="flex items-center justify-center gap-4 m-2">
					<button class="cursor-pointer rounded-full px-6 py-2 font-semibold" :class="activeGroup === 0
						? 'bg-[var(--color-accent)] text-[var(--color-text-alt)]'
						: 'bg-[var(--color-element)] text-[var(--color-text)]'" @click="setActiveGroup(0)">
						Fun
					</button>
					<button v-if="leaderboard.groups.length == 2"
						class="cursor-pointer rounded-full px-6 py-2 font-semibold" :class="activeGroup === 1
							? 'bg-[var(--color-accent)] text-[var(--color-text-alt)]'
							: 'bg-[var(--color-element)] text-[var(--color-text)]'" @click="setActiveGroup(1)">
						{{ $t("teams.pro") }}
					</button>
				</div>

				<div class="grid grid-cols-4 bg-[var(--color-element)] rounded-full py-2 px-4 text-center font-bold">
					<div>{{ $t("result.placement") }}</div>
					<div>{{ $t("result.team") }}</div>
					<div>{{ $t("result.win") }}</div>
					<div>{{ $t("result.points") }}</div>
				</div>
			</div>

			<div class="flex-1 overflow-y-auto mt-2 flex flex-col gap-3 pb-[calc(env(safe-area-inset-bottom))]">
				<div v-for="team in leaderboard.groups[activeGroup].teams"
					class="grid grid-cols-4 text-xl items-center bg-[var(--color-element)] rounded-4xl h-18 py-2 px-4 text-center">
					<div class="rounded-full w-8 h-8 mx-auto flex items-center justify-center" :class="{
						'bg-yellow-500 text-[var(--color-text)]': team.rank === 1,
						'bg-gray-400': team.rank === 2,
						'bg-amber-700 text-[var(--color-text)]': team.rank === 3,
						'bg-[var(--color-background)]': team.rank > 3,
					}">
						{{ team.rank }}
					</div>
					<div>{{ team.id }}</div>
					<div>{{ team.wins }}</div>
					<div :class="{
						'text-green-500': team.points > 0,
						'text-red-500': team.points < 0,
						'text-gray-500': team.points === 0,
					}">
						{{ team.points > 0 ? "+" : "" }}{{ team.points }}
					</div>
				</div>
			</div>
		</div>

		<div v-else-if="!syncGames" id="dashboard-container"
			class="flex flex-col w-full align-center justify-between items-center h-full">
			<button class="colorButton cursor-pointer w-full max-w-100" @click="toggleSyncGames">
				<span>{{ $t("home.sync") }}</span>
				<IconQrCode />
			</button>
			<button class="colorButton cursor-pointer w-full max-w-100" @click="evalTournament">
				<span>{{ $t("home.results") }}</span>
				<IconTrophy />
			</button>
		</div>

		<div v-else id="synchronize-games-container" class="flex flex-col items-center overflow-y-auto">
			<h2 class="text-lg text-center lg:text-xl font-bold mx-4 mb-4">{{ $t("sync.offline") }}</h2>
			<div class="flex justify-center items-center w-full">
				<div
					class="flex flex-col items-center justify-center w-full max-w-50 aspect-square rounded-4xl bg-[var(--color-element)]">

					<IconCamera v-if="!scannerActive" class="w-30 h-30"></IconCamera>
					<qrcode-stream v-else @detect="onDetect"></qrcode-stream>
				</div>
			</div>
			<div class="flex flex-col items-center justify-center gap-4 mt-4">
				<h2 class="font-medium">
					{{ $t("sync.code") }}
					<span class="text-[var(--color-accent)]">{{ store.tournament.id }}</span>
				</h2>
				<qrcode-vue class="" :value="qrvalue" :size="qrSize" level="L" render-as="svg" />
			</div>
		</div>
	</div>
</template>
