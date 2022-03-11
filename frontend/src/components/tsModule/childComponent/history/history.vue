<template>
    <div id="History" :class="historyStyle">
        <div id="HistoryHead" class="HistoryHead"> History
        </div>
        <div id="HistoryContent" class="HistoryContent">
            <svg id="history" style="height:100%;width:100%;float:left">
            
            <g id="nodes"/>
            <g id="edges"/>
            <defs>
                <marker id="markerArrow" markerUnits="strokeWidth" markerWidth="12" markerHeight="12" viewBox="0 0 12 12" refX="6"
                    refY="6" orient="auto">
                    <path d="M2,2 L10,6 L2,10 L2,2" style="fill: #67C23A;" />
                </marker>
                <linearGradient id="savedLinear" x1="0%" y1="0%" x2="0%" y2="100%"> <stop offset="30%" stop-color="#ffffff"/> <stop offset="100%" stop-color="rgb(103, 194, 58)"/> </linearGradient>
                <linearGradient id="notSavedLinear" x1="0%" y1="0%" x2="0%" y2="100%"> <stop offset="30%" stop-color="#ffffff"/> <stop offset="100%" stop-color="#EB6100"/> </linearGradient>
            </defs>
            <defs>
            <filter id="blur-2px" x="-15%" y="-20%"  width="130%" height="140%">
                <feGaussianBlur
                in="SourceGraphic"
                stdDeviation="10" />
            </filter>
            </defs>
            <defs>
            <radialGradient id="grey_blue" cx="50%" cy="50%" r="50%"
            fx="50%" fy="50%">
                <stop offset="0%" style="stop-color:rgb(200,200,200);
                stop-opacity:0"/>
                <stop offset="100%" style="stop-color:rgb(0,0,255);
                stop-opacity:1"/>
            </radialGradient>
            </defs>

            <g id="draw" style="height:100%;width:100%" />
        </svg>
        </div>
        <aside style="height:100px">
            <div>
            <div id="Accuracy"/>
            <div id="Loss"/>
            <div id="Saved"/>
            <div id="NotSaved"/>
            </div>
        </aside>
    </div>
</template>