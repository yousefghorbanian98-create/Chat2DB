## gh-protocol E2E log — 2026-10-24T15:05:19Z

### gradle-build.log (tail)
Downloading https://services.gradle.org/distributions/gradle-8.10.2-bin.zip
.............10%.............20%.............30%.............40%.............50%.............60%.............70%.............80%.............90%.............100%

Welcome to Gradle 8.10.2!

Here are the highlights of this release:
 - Support for Java 23
 - Faster configuration cache
 - Better configuration cache reports

For more details see https://docs.gradle.org/8.10.2/release-notes.html

To honour the JVM settings for this build a single-use Daemon process will be forked. For more on this, please refer to https://docs.gradle.org/8.10.2/userguide/gradle_daemon.html#sec:disabling_the_daemon in the Gradle documentation.
Daemon will be stopped at the end of the build 
Calculating task graph as no cached configuration is available for tasks: assembleDebug
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:parseDebugLocalResources
> Task :app:mapDebugSourceSetPaths
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:checkDebugAarMetadata
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:mergeDebugAssets
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugJniLibFolders
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugResources
> Task :app:compressDebugAssets
> Task :app:mergeDebugNativeLibs
> Task :app:mergeExtDexDebug
> Task :app:processDebugResources
> Task :app:mergeLibDexDebug
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:64:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_2-1792852749223.json

BUILD SUCCESSFUL in 2m 29s
37 actionable tasks: 37 executed
Configuration cache entry stored.

### e2e.log
== adb devices ==
== wait for emulator to reach device state ==
emulator ready after ~4s
List of devices attached
emulator-5554	device

== install APK ==
Performing Streamed Install
Success
== launch app ==
  bash arg: -p
  bash arg: com.ghprotocol.app
  bash arg: -c
  bash arg: android.intent.category.LAUNCHER
  bash arg: 1
args: [-p, com.ghprotocol.app, -c, android.intent.category.LAUNCHER, 1]
 arg: "-p"
 arg: "com.ghprotocol.app"
 arg: "-c"
 arg: "android.intent.category.LAUNCHER"
 arg: "1"
data="com.ghprotocol.app"
data="android.intent.category.LAUNCHER"
Events injected: 1
## Network stats: elapsed time=1935ms (0ms mobile, 0ms wifi, 1935ms not connected)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== VPN consent dialog (tap Allow) ==
WARN: consent dialog not seen (may have been auto-granted or missed)
== wait for tunnel (Xray process + :10808 listening) ==
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
root             1     0   10887764  12548 0                   0 S init
root             2     0          0      0 0                   0 S [kthreadd]
root             3     2          0      0 0                   0 I [rcu_gp]
root             4     2          0      0 0                   0 I [slub_flushwq]
root             5     2          0      0 0                   0 I [netns]
root             7     2          0      0 0                   0 I [kworker/0:0H-events_highpri]
root             9     2          0      0 0                   0 I [mm_percpu_wq]
root            10     2          0      0 0                   0 I [kworker/u4:1-phy1]
root            11     2          0      0 0                   0 I [rcu_tasks_kthread]
root            12     2          0      0 0                   0 I [rcu_tasks_trace_kthread]
root            13     2          0      0 0                   0 S [ksoftirqd/0]
root            14     2          0      0 0                   0 R [rcu_preempt]
root            15     2          0      0 0                   0 S [rcub/0]
root            16     2          0      0 0                   0 S [rcu_exp_gp_kthread_worker]
root            17     2          0      0 0                   0 S [rcu_exp_par_gp_kthread_worker]
root            18     2          0      0 0                   0 S [migration/0]
root            20     2          0      0 0                   0 S [cpuhp/0]
root            21     2          0      0 0                   0 S [cpuhp/1]
root            22     2          0      0 0                   0 S [migration/1]
root            23     2          0      0 0                   0 S [ksoftirqd/1]
root            26     2          0      0 0                   0 I [inet_frag_wq]
root            27     2          0      0 0                   0 S [kauditd]
root            28     2          0      0 0                   0 S [khungtaskd]
root            29     2          0      0 0                   0 S [oom_reaper]
root            30     2          0      0 0                   0 I [writeback]
root            31     2          0      0 0                   0 S [kcompactd0]
root            32     2          0      0 0                   0 S [khugepaged]
root            33     2          0      0 0                   0 I [cryptd]
root            34     2          0      0 0                   0 I [kblockd]
root            35     2          0      0 0                   0 I [blkcg_punt_bio]
root            37     2          0      0 0                   0 I [edac-poller]
root            38     2          0      0 0                   0 I [devfreq_wq]
root            39     2          0      0 0                   0 S [watchdogd]
root            40     2          0      0 0                   0 I [kworker/1:1H-kblockd]
root            42     2          0      0 0                   0 S [kswapd0]
root            44     2          0      0 0                   0 S [erofs_worker/0]
root            45     2          0      0 0                   0 S [erofs_worker/1]
root            46     2          0      0 0                   0 I [kthrotld]
root            47     2          0      0 0                   0 S [dmabuf-deferred-free-worker]
root            48     2          0      0 0                   0 I [uas]
root            49     2          0      0 0                   0 I [dm_bufio_cache]
root            50     2          0      0 0                   0 I [kworker/0:1H-kblockd]
root            51     2          0      0 0                   0 I [mld]
root            52     2          0      0 0                   0 I [ipv6_addrconf]
root            54     2          0      0 0                   0 I [kworker/1:2-virtio_vsock]
root            55     2          0      0 0                   0 S [khvcd]
root            56     2          0      0 0                   0 S [hwrng]
root            57     2          0      0 0                   0 S [jbd2/vdd1-8]
root            58     2          0      0 0                   0 I [ext4-rsv-conver]
root            60     2          0      0 0                   0 I [kdmflush/254:0]
root            61     2          0      0 0                   0 I [kdmflush/254:1]
root            62     2          0      0 0                   0 I [kdmflush/254:2]
root            63     2          0      0 0                   0 I [kdmflush/254:3]
root            64     2          0      0 0                   0 I [kdmflush/254:4]
root            65     2          0      0 0                   0 I [kdmflush/254:5]
root            66     2          0      0 0                   0 I [kverityd]
root            67     2          0      0 0                   0 I [kworker/1:2H-kverityd]
root            68     2          0      0 0                   0 I [ext4-rsv-conver]
root            69     2          0      0 0                   0 I [ext4-rsv-conver]
root            70     2          0      0 0                   0 I [ext4-rsv-conver]
root            71     2          0      0 0                   0 I [ext4-rsv-conver]
root            73     1   10885756   7888 0                   0 S init
root            74     1   10849124   8528 0                   0 S ueventd
root            79     2          0      0 0                   0 I [kdmflush/254:6]
root            80     2          0      0 0                   0 I [kdmflush/254:7]
root            82     2          0      0 0                   0 I [kdmflush/254:9]
root            83     2          0      0 0                   0 I [kdmflush/254:10]
root            84     2          0      0 0                   0 I [kdmflush/254:11]
root            85     2          0      0 0                   0 I [kdmflush/254:12]
root            86     2          0      0 0                   0 I [kdmflush/254:13]
root            88     2          0      0 0                   0 I [kdmflush/254:15]
root            90     2          0      0 0                   0 I [kdmflush/254:17]
root            91     2          0      0 0                   0 I [kdmflush/254:18]
root            93     2          0      0 0                   0 I [kdmflush/254:20]
root            94     2          0      0 0                   0 I [kdmflush/254:21]
root            96     2          0      0 0                   0 I [kdmflush/254:23]
root            97     2          0      0 0                   0 I [kdmflush/254:24]
root           100     2          0      0 0                   0 I [kdmflush/254:27]
root           101     2          0      0 0                   0 I [kdmflush/254:28]
root           103     2          0      0 0                   0 I [kdmflush/254:30]
root           107     2          0      0 0                   0 I [kdmflush/254:34]
root           109     2          0      0 0                   0 I [kdmflush/254:36]
root           110     2          0      0 0                   0 I [kdmflush/254:37]
root           115     2          0      0 0                   0 I [ext4-rsv-conver]
root           116     2          0      0 0                   0 I [ext4-rsv-conver]
root           117     2          0      0 0                   0 I [ext4-rsv-conver]
root           118     2          0      0 0                   0 I [kworker/u4:3-phy1]
root           119     2          0      0 0                   0 I [ext4-rsv-conver]
root           124     2          0      0 0                   0 I [kworker/0:2-virtio_vsock]
prng_seeder    125     1   10913416   6660 0                   0 S prng_seeder
root           127     2          0      0 0                   0 S [sugov:0]
root           128     2          0      0 0                   0 S [sugov:1]
root           129     2          0      0 0                   0 S [irq/18-goldfish_pipe_dprctd]
logd           130     1   10845116   8552 0                   0 S logd
lmkd           131     1   10806556   3252 0                   0 S lmkd
system         132     1   10880976   5812 0                   0 S servicemanager
system         133     1   10854128   6960 0                   0 S hwservicemanager
root           135     2          0      0 0                   0 S [psimon]
shell          139     1   10797644   3376 wait_woken          0 S sh
root           140     1   10782656   2956 0                   0 S qemu-props
root           141     1   10875516  10088 0                   0 S vold
root           148     2          0      0 0                   0 I [kdmflush/254:38]
system         153     1   10880908   5672 0                   0 S android.system.suspend-service
keystore       154     1   10993740  15784 0                   0 S keystore2
system         155     1   10835916   4912 0                   0 S android.hardware.atrace@1.0-service
root           156     2          0      0 0                   0 I [cfg80211]
nobody         157     1   10918520   8872 0                   0 S android.hardware.security.keymint-service
root           179     2          0      0 0                   0 I [blk_crypto_wq]
root           181     2          0      0 0                   0 I [usbip_event]
root           188     2          0      0 0                   0 S [jbd2/dm-38-8]
root           189     2          0      0 0                   0 I [ext4-rsv-conver]
tombstoned     195     1   10818940   2552 0                   0 S tombstoned
root           226     2          0      0 0                   0 I [ext4-rsv-conver]
root           227     2          0      0 0                   0 I [ext4-rsv-conver]
root           238     2          0      0 0                   0 I [ext4-rsv-conver]
root           239     2          0      0 0                   0 I [kverityd]
root           240     2          0      0 0                   0 I [ext4-rsv-conver]
root           241     2          0      0 0                   0 I [ext4-rsv-conver]
root           242     2          0      0 0                   0 I [ext4-rsv-conver]
root           243     2          0      0 0                   0 I [ext4-rsv-conver]
root           244     2          0      0 0                   0 I [ext4-rsv-conver]
root           245     2          0      0 0                   0 I [ext4-rsv-conver]
root           246     2          0      0 0                   0 I [ext4-rsv-conver]
root           247     2          0      0 0                   0 I [ext4-rsv-conver]
root           248     2          0      0 0                   0 I [ext4-rsv-conver]
root           249     2          0      0 0                   0 I [kverityd]
root           250     2          0      0 0                   0 I [ext4-rsv-conver]
root           251     2          0      0 0                   0 I [kverityd]
root           252     2          0      0 0                   0 I [ext4-rsv-conver]
root           253     2          0      0 0                   0 I [kverityd]
root           254     2          0      0 0                   0 I [ext4-rsv-conver]
root           255     2          0      0 0                   0 I [kverityd]
root           256     2          0      0 0                   0 I [ext4-rsv-conver]
root           257     2          0      0 0                   0 I [kverityd]
root           258     2          0      0 0                   0 I [ext4-rsv-conver]
root           259     2          0      0 0                   0 I [kverityd]
root           260     2          0      0 0                   0 I [ext4-rsv-conver]
root           261     2          0      0 0                   0 I [kverityd]
root           262     2          0      0 0                   0 I [ext4-rsv-conver]
root           263     2          0      0 0                   0 I [kverityd]
root           264     2          0      0 0                   0 I [ext4-rsv-conver]
root           265     2          0      0 0                   0 I [kverityd]
root           266     2          0      0 0                   0 I [ext4-rsv-conver]
root           267     2          0      0 0                   0 I [ext4-rsv-conver]
root           268     2          0      0 0                   0 I [kverityd]
root           269     2          0      0 0                   0 I [ext4-rsv-conver]
root           270     2          0      0 0                   0 I [kverityd]
root           271     2          0      0 0                   0 I [ext4-rsv-conver]
root           272     2          0      0 0                   0 I [kverityd]
root           273     2          0      0 0                   0 I [ext4-rsv-conver]
root           274     2          0      0 0                   0 I [kverityd]
root           275     2          0      0 0                   0 I [ext4-rsv-conver]
root           276     2          0      0 0                   0 I [kverityd]
root           277     2          0      0 0                   0 I [ext4-rsv-conver]
root           278     2          0      0 0                   0 I [kverityd]
root           279     2          0      0 0                   0 I [ext4-rsv-conver]
root           280     2          0      0 0                   0 I [kverityd]
root           281     2          0      0 0                   0 I [ext4-rsv-conver]
root           282     2          0      0 0                   0 I [kverityd]
root           283     2          0      0 0                   0 I [ext4-rsv-conver]
root           284     2          0      0 0                   0 I [kverityd]
root           285     2          0      0 0                   0 I [kverityd]
root           286     2          0      0 0                   0 I [ext4-rsv-conver]
root           287     2          0      0 0                   0 I [ext4-rsv-conver]
root           315     1   10780244   3084 0                   0 S dhcpclient
statsd         326     1   10863436   6108 0                   0 S statsd
root           327     1   10959232  12352 0                   0 S netd
root           328     1   14264136 177692 0                   0 S zygote64
system         329     1   10876176   3248 0                   0 S android.hidl.allocator@1.0-service
audioserver    330     1   11146680  14780 0                   0 S android.hardware.audio.service
hsm            333     1   10883048   3672 0                   0 S android.hardware.authsecret-service.example
system         335     1   10912700  11404 0                   0 S android.hardware.camera.provider.ranchu
system         336     1   10971308  15700 0                   0 S android.hardware.camera.provider@2.7-service-google
system         337     1   10864208   5468 0                   0 S android.hardware.gatekeeper@1.0-service.software
system         338     1   10866632  14804 0                   0 S android.hardware.graphics.allocator@3.0-service.ranchu
system         339     1   10905652   6312 0                   0 S android.hardware.health-service.example
media          340     1   10997092  17412 0                   0 S android.hardware.media.c2@1.0-service-goldfish
system         341     1   10920156  11204 0                   0 S android.hardware.neuralnetworks-service-sample-all
system         342     1   11003896   8820 0                   0 S android.hardware.neuralnetworks-service-sample-limited
system         345     1   10840940  10980 0                   0 S android.hardware.neuralnetworks-shim-service-sample
system         346     1   10852612   6952 0                   0 S android.hardware.sensors-service.multihal
system         347     1   10842288   5288 0                   0 S android.hardware.thermal@2.0-service.mock
system         348     1   10792540   5248 0                   0 S android.hardware.usb-service.example
wifi           349     1   10817000   6288 0                   0 S android.hardware.wifi-service
bluetooth      350     1   10955376   6456 0                   0 S android.hardware.bluetooth-service.default
root           351   327   10783912   3548 0                   0 S iptables-restore
root           352   327   10794152   3528 0                   0 S ip6tables-restore
media          353     1   10895680   5468 0                   0 S android.hardware.cas-service.example
context_hub    357     1   10811432   3668 0                   0 S android.hardware.contexthub-service.example
nobody         358     1   10825676   4964 0                   0 S android.hardware.biometrics.face-service.example
system         359     1   10923828  29212 0                   0 S android.hardware.graphics.composer3-service.ranchu
nobody         360     1   10815472   6240 0                   0 S android.hardware.identity-service.example
nobody         361     1   10781040   5316 0                   0 S android.hardware.lights-service.example
nobody         362     1   10781068   5396 0                   0 S android.hardware.power-service.example
system         365     1   10874924   5332 0                   0 S android.hardware.power.stats-service.example
system         366     1   10885236   4436 0                   0 S android.hardware.rebootescrow-service.default
nobody         368     1   10830276   5228 0                   0 S android.hardware.vibrator-service.example
audioserver    369     1   11174652  27196 0                   0 S audioserver
credstore      373     1   10884712   7868 0                   0 S credstore
gpu_service    382     1   10803004   8444 0                   0 S gpuservice
system         389     1   11191992  40396 0                   0 S surfaceflinger
shell          406     1   10811748  10668 0                   0 S adbd
nobody         408     1   10801276   3912 0                   0 S traced_probes
nobody         409     1   10884736   3968 0                   0 S traced
logd           413     1   10825372   4128 0                   0 S logcat
bluetooth      414     1   10792904   2988 0                   0 S bt_vhci_forwarder
cameraserver   419     1   11227284  28148 0                   0 S cameraserver
incidentd      431     1   10814536   5856 0                   0 S incidentd
root           436     1   10857240   7464 0                   0 S installd
mediaex        439     1   11295228  29168 0                   0 S media.extractor
media          442     1   10844164   8772 0                   0 S media.metrics
media          443     1   11408464  31100 0                   0 S mediaserver
root           445     1   10901036   6104 0                   0 S storaged
wifi           446     1   10833072   7772 0                   0 S wificond
radio          447     1   10982748  17404 0                   0 S libgoldfish-rild
mediacodec     450     1   11344512  30932 0                   0 S media.swcodec
mdnsr          467     1   10806496   3876 0                   0 S mdnsd
system         469     1   10804692   6372 0                   0 S gatekeeperd
system         545   328   15473080 356680 0                   0 S system_server
wifi           935     1   10877744  10616 0                   0 S wpa_supplicant
u0_a116        954   328   13762932 249840 0                   0 R com.android.systemui
webview_zygote 1116  328   14206468  94088 0                   0 S webview_zygote
gps           1131     1   10781720   5680 0                   0 S android.hardware.gnss-service.ranchu
network_stack 1140   328   13577236 119428 0                   0 S com.android.networkstack.process
secure_element 1189  328   13560048  95644 0                   0 S com.android.se
system        1209   328   13711908 146916 0                   0 S com.android.settings
system        1292     1   10866392   5548 0                   0 S android.hardware.biometrics.fingerprint-service.ranchu
u0_a112       1299   328   13699724 189244 0                   0 S com.android.launcher3
u0_a130       1429   328   13580096 111776 0                   0 S com.android.cellbroadcastreceiver.module
u0_a109       1440   328   13581840 119684 0                   0 S com.android.inputmethod.latin
u0_a64        1484   328   13564192  92128 0                   0 S com.android.cellbroadcastreceiver
root          1537     2          0      0 0                   0 I [kworker/u5:1-blk_crypto_wq]
shell         1613   406   10827760   3676 unix_stream_read_generic 0 S abb
system        1732   328   13559232  91652 0                   0 S com.android.emulator.multidisplay
u0_a71        1949   328   13558336  94740 0                   0 S com.android.externalstorage
u0_a65        2009   328   13562440 104632 0                   0 S android.process.media
u0_a121       2053   328   13659020 128924 0                   0 S com.android.providers.media.module
u0_a134       2121   328   13560832  94156 0                   0 S android.ext.services
u0_a57        2467   328   13570340 114036 0                   0 S android.process.acore
u0_a94        2489   328   13566860  95208 0                   0 S com.android.imsserviceentitlement
system        2491   328   13559440  92256 0                   0 S com.android.dynsystem:dynsystem
u0_a66        2608   328   13559936  91568 0                   0 S com.android.packageinstaller
u0_a128       2632   328   13573272 103676 0                   0 S com.android.rkpdapp
shell         2661   328   13558004  89720 0                   0 S com.android.shell
u0_a58        2680   328   13566540  97044 0                   0 S com.android.statementservice
u0_a108       2721   328   13571812 112384 0                   0 S com.android.messaging
radio         2911   328   13610296 140744 0                   0 S com.android.phone
u0_a138       3002   328   13590988 118276 0                   0 S com.android.permissioncontroller
root          3151     2          0      0 0                   0 I [kworker/0:0-cgroup_destroy]
u0_a111       3233   328   13558676  93340 0                   0 S com.android.carrierconfig
u0_a102       3347   328   13562892  92960 0                   0 S com.android.music
u0_a82        3443   328   13558724  93108 0                   0 S com.android.carrierdefaultapp
root          3645     2          0      0 0                   0 I [kworker/u5:0-hci0]
root          3747     2          0      0 0                   0 I [kworker/u4:2-phy1]
root          4168     2          0      0 0                   0 I [kworker/1:0-virtio_vsock]
root          4441     2          0      0 0                   0 I [kworker/0:1-mm_percpu_wq]
root          4745     2          0      0 0                   0 R [kworker/u4:0+events_unbound]
root          4995     2          0      0 0                   0 I [kworker/1:1-virtio_vsock]
bluetooth     5142   328   13671268 112284 0                   0 R com.android.bluetooth
shell         5171   406   10770264   3624 0                   0 R ps
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
=== E2E FAILED: tunnel not up (xray/:10808) ===


