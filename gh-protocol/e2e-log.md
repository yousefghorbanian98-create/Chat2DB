## gh-protocol E2E log — 2026-10-25T16:37:48Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T16:36:03Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 16:27 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 16:36 .
drwxr-xr-x 3 runner runner 4096 Oct 25 16:36 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 16:36 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 16:36 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.12.0 (build_id 16428233) (CL:N/A)
INFO         | Graphics backend: gfxstream
INFO         | Found systemPath /usr/local/lib/android/sdk/system-images/android-34/google_apis/x86_64/
INFO         | Saving last run QEMU version for the AVD to 2
INFO         | Changing default hw.initialOrientation to portrait

INFO         | Increasing RAM size to 4096MB
##############################################################################
##                        WARNING - ACTION REQUIRED                         ##
##  Consider using the '-metrics-collection' flag to help improve the       ##
##  emulator by sending anonymized usage data. Or use the '-no-metrics'     ##
##  flag to bypass this warning and turn off the metrics collection.        ##
##  In a future release this warning will turn into a one-time blocking     ##
##  prompt to ask for explicit user input regarding metrics collection.     ##
##                                                                          ##
##  Please see '-help-metrics-collection' for more details. You can use     ##
##  '-metrics-to-file' or '-metrics-to-console' flags to see what type of   ##
##  data is being collected by emulator as part of usage statistics.        ##
##############################################################################
INFO         | Guest GLES Driver: Auto (ext controls)
INFO         | emuglConfig_init: vulkan_mode_selected:swiftshader gles_mode_selected:swiftshader
INFO         | Checking system compatibility:
INFO         |   Checking: hasSufficientDiskSpace
INFO         |      Ok: Disk space requirements to run avd: `gh_test` are met
INFO         |   Checking: hasSufficientHwGpu
INFO         |      Ok: Hardware GPU compatibility checks are not required
INFO         |   Checking: hasSufficientSystem
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3095
INFO         | Initializing gfxstream backend
INFO         | startOpenglesRendererImpl: gpu info
INFO         | 
INFO         | Vulkan 1.4 is not supported for the guest and won't be enabled
INFO         | initIcdPaths: ICD set to 'swiftshader', using Swiftshader ICD
INFO         | Setting ICD filenames for the loader = /usr/local/lib/android/sdk/emulator/lib64/vulkan/vk_swiftshader_icd.json
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so.1]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so]
INFO         | Added library: /usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so
INFO         | Selecting Vulkan device: SwiftShader Device (Subzero), Version: 1.3.0
INFO         | Using Vulkan externalMemoryMode: OpaqueFd for VkEmulation
INFO         | Format VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16 does not support YCbCr sampler conversion
INFO         | SharedLibrary::open for [libX11]
WARNING      | Could not open libX11.so, try libX11.so.6
INFO         | SharedLibrary::open for [libX11.so.6]
INFO         | SharedLibrary::open for [libX11-xcb]
WARNING      | Could not open libX11-xcb.so, try libX11-xcb.so.1
INFO         | SharedLibrary::open for [libX11-xcb.so.1]
INFO         | Initializing VkEmulation features:
INFO         |     glInteropSupported: false
INFO         |     useDeferredCommands: true
INFO         |     createResourceWithRequirements: true
INFO         |     useVulkanComposition: false
INFO         |     useVulkanNativeSwapchain: false
INFO         |     enable guestRenderDoc: false
INFO         |     ASTC LDR emulation mode: Gpu
INFO         |     enable ETC2 emulation: true
INFO         |     enable Ycbcr emulation: false
INFO         |     guestVulkanOnly: false
INFO         |     useDedicatedAllocations: false
INFO         |     guestVulkanMaxApiVersion: 1.3.0
INFO         |     enableProtectedMemoryEmulation: false
INFO         | Graphics Adapter Vendor Google (Google Inc.)
INFO         | Graphics Adapter Android Emulator OpenGL ES Translator (Google SwiftShader)
INFO         | Graphics API Version OpenGL ES 3.0 (OpenGL ES 3.0 SwiftShader 4.0.0.1)
INFO         | Graphics API Extensions GL_OES_EGL_sync GL_OES_EGL_image GL_OES_EGL_image_external GL_OES_depth24 GL_OES_depth32 GL_OES_element_index_uint GL_OES_texture_float GL_OES_texture_float_linear GL_OES_compressed_paletted_texture GL_OES_compressed_ETC1_RGB8_texture GL_OES_depth_texture GL_OES_texture_half_float GL_OES_texture_half_float_linear GL_OES_packed_depth_stencil GL_OES_vertex_half_float GL_OES_standard_derivatives GL_OES_texture_npot GL_OES_rgb8_rgba8 GL_EXT_color_buffer_float GL_EXT_color_buffer_half_float GL_EXT_texture_format_BGRA8888 GL_APPLE_texture_format_BGRA8888 
INFO         | Graphics Device Extensions N/A
INFO         | Disabling sparse binding feature support
WARNING      | No adb private key exists
INFO         | Userspace boot properties:
INFO         |   androidboot.boot_devices=pci0000:00/0000:00:03.0 pci0000:00/0000:00:06.0
INFO         |   androidboot.dalvik.vm.heapsize=576m
INFO         |   androidboot.debug.hwui.renderer=skiagl
INFO         |   androidboot.debug.sf.nobootanimation=1
INFO         |   androidboot.hardware=ranchu
INFO         |   androidboot.hardware.gltransport=pipe
INFO         |   androidboot.hardware.vulkan=ranchu
INFO         |   androidboot.logcat=*:V
INFO         |   androidboot.opengles.version=196608
INFO         |   androidboot.qemu=1
INFO         |   androidboot.qemu.avd_name=gh_test
INFO         |   androidboot.qemu.camera_hq_edge_processing=0
INFO         |   androidboot.qemu.camera_protocol_ver=1
INFO         |   androidboot.qemu.cpuvulkan.version=4210688
INFO         |   androidboot.qemu.gltransport.drawFlushInterval=800
INFO         |   androidboot.qemu.gltransport.name=pipe
INFO         |   androidboot.qemu.hwcodec.avcdec=2
INFO         |   androidboot.qemu.hwcodec.hevcdec=2
INFO         |   androidboot.qemu.hwcodec.vpxdec=2
INFO         |   androidboot.qemu.settings.system.screen_off_timeout=2147483647
INFO         |   androidboot.qemu.skin=1080x2400
INFO         |   androidboot.qemu.virtiowifi=1
INFO         |   androidboot.qemu.vsync=60
INFO         |   androidboot.serialno=EMULATOR37X2X12X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x7f04da401000 as it is in the protected range from 0x7f03da400000 to 0x7f04da600000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Successfully initialized netsim WiFi
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 38519 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 123
ERROR        | Failed to bind to texture: invalid color buffer.
ERROR        | Failed to find ColorBuffer: 131
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 3095) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:37231 is gone due to Stream removed (CANCELLED)

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
> Task :app:preBuild UP-TO-DATE
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:packageDebugResources
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugResources
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugAssets
> Task :app:parseDebugLocalResources
> Task :app:checkDebugDuplicateClasses
> Task :app:compressDebugAssets
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/ui/HomeViewModel.kt:520:17 Condition is always 'true'.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792945979062.json

BUILD SUCCESSFUL in 2m 53s
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
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 20s) ==
emulator can reach raw.githubusercontent.com after ~16s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3141)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tapped VPN consent at: 894 1519 (iter 2)
tunnel up after ~8s (xray pid + :10808 listener)
== wait for VpnService establish (consent result) ==
vpn established after ~6s
18: tun0: <POINTOPOINT,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 10.8.0.2/24 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fd00:1::1/128 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::e9cc:c7af:5143:9d41/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.114.4): 56(84) bytes.

--- 140.82.114.4 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
--------- beginning of main
10-25 16:37:29.694  3141  3141 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 16:37:29.701  3141  3141 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 16:37:30.194  3141  3141 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 16:37:30.236  3141  3141 D GhDiag  : connect: config written bytes=5134 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 16:37:30.317  3141  3141 D GhDiag  : connect: core.start=true 
10-25 16:37:38.770  3141  3141 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 16:37:38.809  3141  3141 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@dec7e59} — relay loop started
10-25 16:37:39.010  3141  3280 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (81ms)
10-25 16:37:39.170  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.227  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 16:37:39.228  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 16:37:39.233  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.283  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=80
10-25 16:37:39.318  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.519  3141  4493 D GhDiag  : relay dns -> 178B ok
10-25 16:37:39.519  3141  4494 D GhDiag  : relay dns -> 274B ok
10-25 16:37:39.635  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.704  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:40.089  3141  4462 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 16:37:40.202  3141  4500 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 16:37:40.203  3141  4462 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 16:37:40.203  3141  4462 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 16:37:40.228  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:40.728  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:41.426  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:41.750  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:42.774  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:42.937  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:42.949  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:42.962  3141  4561 D GhDiag  : relay dns -> 168B ok
10-25 16:37:43.078  3141  4562 D GhDiag  : relay dns -> 152B ok
10-25 16:37:43.085  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=60
10-25 16:37:43.165  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:43.165  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:43.167  3141  4566 D GhDiag  : relay tcp 34.153.x.x:443 -> socks5 ok
10-25 16:37:43.180  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=40
10-25 16:37:43.181  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=576
10-25 16:37:43.194  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=76
10-25 16:37:43.211  3141  4568 D GhDiag  : relay dns -> 168B ok
10-25 16:37:43.213  3141  4567 D GhDiag  : relay dns -> 264B ok
10-25 16:37:43.225  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=40
10-25 16:37:43.338  3141  4570 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 16:37:29.694  3141  3141 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 16:37:29.701  3141  3141 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 16:37:30.194  3141  3141 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 16:37:30.236  3141  3141 D GhDiag  : connect: config written bytes=5134 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 16:37:30.317  3141  3141 D GhDiag  : connect: core.start=true 
10-25 16:37:38.770  3141  3141 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 16:37:38.809  3141  3141 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@dec7e59} — relay loop started
10-25 16:37:39.010  3141  3280 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (81ms)
10-25 16:37:39.170  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.227  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 16:37:39.228  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 16:37:39.233  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.283  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=80
10-25 16:37:39.318  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.519  3141  4493 D GhDiag  : relay dns -> 178B ok
10-25 16:37:39.519  3141  4494 D GhDiag  : relay dns -> 274B ok
10-25 16:37:39.635  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.704  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:40.089  3141  4462 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 16:37:40.202  3141  4500 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 16:37:40.203  3141  4462 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 16:37:40.203  3141  4462 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 16:37:40.228  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:40.728  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:41.426  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:41.750  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:42.774  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:42.937  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:42.949  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:42.962  3141  4561 D GhDiag  : relay dns -> 168B ok
10-25 16:37:43.078  3141  4562 D GhDiag  : relay dns -> 152B ok
10-25 16:37:43.085  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=60
10-25 16:37:43.165  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:43.165  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:43.167  3141  4566 D GhDiag  : relay tcp 34.153.x.x:443 -> socks5 ok
10-25 16:37:43.180  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=40
10-25 16:37:43.181  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=576
10-25 16:37:43.194  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=76
10-25 16:37:43.211  3141  4568 D GhDiag  : relay dns -> 168B ok
10-25 16:37:43.213  3141  4567 D GhDiag  : relay dns -> 264B ok
10-25 16:37:43.225  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=40
10-25 16:37:43.338  3141  4570 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 16:37:45.944  3141  4643 D GhDiag  : relay dns -> 260B ok
10-25 16:37:45.953  3141  4644 D GhDiag  : relay dns -> 164B ok
10-25 16:37:46.171  3141  4645 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 16:37:46.210  3141  4666 D GhDiag  : relay dns -> 256B ok
10-25 16:37:46.221  3141  4665 D GhDiag  : relay dns -> 160B ok
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 16:37:20.769   520   819 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 16:37:20.817   520  2057 D CoreBackPreview: Window{c76fb4c u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@b35ef77, mPriority=0, mIsAnimationCallback=false}
10-25 16:37:21.412   520   548 I ActivityManager: Start proc 3141:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 16:37:21.495  3141  3141 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 16:37:21.504  3141  3141 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 16:37:21.505  3141  3141 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 16:37:21.505  3141  3141 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 16:37:21.567   520   537 V WindowManager: Sent Transition #5 createdAt=10-25 16:37:20.679 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=46467 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{b148aa9 Task{9f335d8 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{1b4b82e com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 16:37:21.567   520   537 V WindowManager:     info={id=5 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{b148aa9 Task{9f335d8 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0x9b290ad sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{b3eb9c7 Task{e5436a6 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0x1b08652 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 16:37:22.048  3141  3141 W ziparchive: Unable to open '/data/app/~~xF1pNm3OkPAsNzIY1rLKfQ==/com.ghprotocol.app-YVMohamxqRvzTDjcrFM18A==/base.dm': No such file or directory
10-25 16:37:22.051  3141  3141 W ziparchive: Unable to open '/data/app/~~xF1pNm3OkPAsNzIY1rLKfQ==/com.ghprotocol.app-YVMohamxqRvzTDjcrFM18A==/base.dm': No such file or directory
10-25 16:37:22.559  3141  3141 D nativeloader: Configuring clns-6 for other apk /data/app/~~xF1pNm3OkPAsNzIY1rLKfQ==/com.ghprotocol.app-YVMohamxqRvzTDjcrFM18A==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~xF1pNm3OkPAsNzIY1rLKfQ==/com.ghprotocol.app-YVMohamxqRvzTDjcrFM18A==/lib/x86_64:/data/app/~~xF1pNm3OkPAsNzIY1rLKfQ==/com.ghprotocol.app-YVMohamxqRvzTDjcrFM18A==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 16:37:22.571  3141  3141 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 16:37:22.571  3141  3141 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 16:37:24.253   520   594 D CoreBackPreview: Window{ccd8c07 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@b3e817d, mPriority=0, mIsAnimationCallback=false}
10-25 16:37:24.645  3141  3141 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 16:37:24.645  3141  3141 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 16:37:24.645  3141  3141 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 16:37:24.660  3141  3141 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 16:37:24.660  3141  3141 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 16:37:24.660  3141  3141 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 16:37:24.660  3141  3141 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 16:37:25.327  1724  1724 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 16:37:25.482   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{c8795e3 com.google.android.youtube/10138} BLOCKED
10-25 16:37:25.483   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{5f82be0 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 16:37:25.483   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{7491e99 com.android.camera2/10146} BLOCKED
10-25 16:37:25.483   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{4cad55e com.google.android.as/10124} BLOCKED
10-25 16:37:25.483   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{c13ad3f com.google.android.gm/10143} BLOCKED
10-25 16:37:25.485   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{e4260c com.google.android.devicelockcontroller/10191} BLOCKED
10-25 16:37:25.485   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{e040b55 com.google.android.dialer/10128} BLOCKED
10-25 16:37:25.486   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{beae96a com.google.android.contacts/10155} BLOCKED
10-25 16:37:25.494   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{81fde5b com.google.android.apps.youtube.music/10156} BLOCKED
10-25 16:37:26.060  1724  1724 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 16:37:26.078  1724  2886 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 16:37:26.078  1724  2886 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 16:37:26.331   520   537 W ziparchive: Unable to open '/data/app/~~xF1pNm3OkPAsNzIY1rLKfQ==/com.ghprotocol.app-YVMohamxqRvzTDjcrFM18A==/base.dm': No such file or directory
10-25 16:37:26.468   520  1188 W InputManager-JNI: Input channel object 'c76fb4c Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 16:37:26.572   520   537 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +5s793ms
10-25 16:37:27.270   520  2169 I ImeTracker: com.ghprotocol.app:e3ae6766: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 16:37:27.270   520  2169 I ImeTracker: com.ghprotocol.app:e3ae6766: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 16:37:27.327  1559  1559 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 16:37:28.802  3141  3636 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 16:37:28.920   520  1929 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 16:37:28.926   833   876 V WindowManagerShell: Transition requested: android.os.BinderProxy@54c74c4 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=54621 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@b99fad} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{a7de2e2 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 16:37:29.150  3669  3669 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 16:37:29.169  3669  3669 I AndroidRuntime: Using default boot image
10-25 16:37:29.169  3669  3669 I AndroidRuntime: Leaving lock profiling enabled
10-25 16:37:29.219   520  1274 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{cb9c92f com.google.android.gm/10143} BLOCKED
10-25 16:37:29.341  3669  3669 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 16:37:29.694  3141  3141 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 16:37:29.701  3141  3141 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 16:37:29.950  3780  3780 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 16:37:29.958  3780  3780 W libxraycore.so: type=1400 audit(0.0:19): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 16:37:29.958  3780  3780 W libxraycore.so: type=1400 audit(0.0:20): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 16:37:29.958  3780  3780 W libxraycore.so: type=1400 audit(0.0:21): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 16:37:30.194  3141  3141 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 16:37:30.236  3141  3141 D GhDiag  : connect: config written bytes=5134 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 16:37:30.317  3141  3141 D GhDiag  : connect: core.start=true 
10-25 16:37:30.332   520  2177 D CoreBackPreview: Window{6d03d98 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@18e496e, mPriority=0, mIsAnimationCallback=false}
10-25 16:37:30.432  3669  3669 D AndroidRuntime: Shutting down VM
10-25 16:37:30.430  3821  3821 W libxraycore.so: type=1400 audit(0.0:26): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 16:37:30.438  3821  3821 W libxraycore.so: type=1400 audit(0.0:27): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 16:37:30.438  3821  3821 W libxraycore.so: type=1400 audit(0.0:28): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 16:37:30.438  3821  3821 W libxraycore.so: type=1400 audit(0.0:29): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 16:37:31.930  3821  3821 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=54779 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 16:37:32.085  3141  3162 I .ghprotocol.app: Background concurrent copying GC freed 102589(5366KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6765KB/13MB, paused 157.721ms,7us total 493.180ms
10-25 16:37:32.234   833   876 V WindowManagerShell: onTransitionReady android.os.BinderProxy@54c74c4: {id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{34085b6 u0 com.ghprotocol.app/.MainActivity)/@0x519d27b sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4f12cbb u0 com.ghprotocol.app/.MainActivity)/@0x424898 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 16:37:32.235   520   537 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s336ms
10-25 16:37:32.235   520   537 V WindowManager: Sent Transition #6 createdAt=10-25 16:37:28.917 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=54621 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{b148aa9 Task{9f335d8 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{24338cf com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 16:37:32.236   833   876 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{34085b6 u0 com.ghprotocol.app/.MainActivity)/@0x519d27b sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4f12cbb u0 com.ghprotocol.app/.MainActivity)/@0x424898 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 16:37:32.237   833   876 V WindowManagerShell: start default transition animation, info = {id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{34085b6 u0 com.ghprotocol.app/.MainActivity)/@0x519d27b sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4f12cbb u0 com.ghprotocol.app/.MainActivity)/@0x424898 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 16:37:32.237   520   537 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{34085b6 u0 com.ghprotocol.app/.MainActivity)/@0x2913ba9 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{4f12cbb u0 com.ghprotocol.app/.MainActivity)/@0xca95330 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 16:37:32.757   833   876 V WindowManagerShell: Transition requested: android.os.BinderProxy@4a80ae5 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=58046 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@fc99ba} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{240506b com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 16:37:32.854   520   540 W ActivityTaskManager: Activity top resumed state loss timeout for ActivityRecord{34085b6 u0 com.ghprotocol.app/.MainActivity t8}
10-25 16:37:32.854   520   540 W ActivityTaskManager: Activity pause timeout for ActivityRecord{34085b6 u0 com.ghprotocol.app/.MainActivity t8}
10-25 16:37:33.014   520  2056 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{b6b68c com.google.android.settings.intelligence/10118} BLOCKED
10-25 16:37:33.024   520  2178 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{5b291d5 com.google.android.settings.intelligence/10118} BLOCKED
10-25 16:37:33.297   520  2057 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 16:37:33.298   520  2057 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 16:37:33.298   520  2057 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 16:37:34.237   520   537 V WindowManager: Sent Transition #7 createdAt=10-25 16:37:32.336 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=58046 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{b148aa9 Task{9f335d8 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{955716a com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 16:37:35.503   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{c8ce6a0 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 16:37:35.503   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{6032259 com.google.android.gm/10143} BLOCKED
10-25 16:37:35.503   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{da2ee1e com.google.android.devicelockcontroller/10191} BLOCKED
10-25 16:37:35.503   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{c20b6ff com.google.android.rkpdapp/10183} BLOCKED
10-25 16:37:35.504   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{9e9cccc com.google.android.settings.intelligence/10118} BLOCKED
10-25 16:37:35.504   520   571 I AppsFilter: interaction: PackageSetting{f982a12 com.ghprotocol.app/10192} -> PackageSetting{582fd2c com.google.android.projection.gearhead/10123} BLOCKED
10-25 16:37:35.702  4174  4174 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 16:37:35.707  4174  4174 I AndroidRuntime: Using default boot image
10-25 16:37:35.707  4174  4174 I AndroidRuntime: Leaving lock profiling enabled
10-25 16:37:35.883  4174  4174 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 16:37:36.814  1462  2766 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 16:37:37.046  4174  4174 D AndroidRuntime: Shutting down VM
10-25 16:37:37.167  1403  3470 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 16:37:38.361   520  1925 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 16:37:38.745   520  2180 I ImeTracker: com.ghprotocol.app:b28cac6: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 16:37:38.745   520  2180 I ImeTracker: com.ghprotocol.app:b28cac6: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 16:37:38.755  1559  1559 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 16:37:38.768   520  1929 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 16:37:38.770  3141  3141 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 16:37:38.808   520   587 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 16:37:38.809  3141  3141 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@dec7e59} — relay loop started
10-25 16:37:39.010  3141  3280 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (81ms)
10-25 16:37:39.170  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.227  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 16:37:39.228  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 16:37:39.233  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.283  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=80
10-25 16:37:39.318  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.519  3141  4493 D GhDiag  : relay dns -> 178B ok
10-25 16:37:39.519  3141  4494 D GhDiag  : relay dns -> 274B ok
10-25 16:37:39.635  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:39.661  3141  3162 I .ghprotocol.app: Background young concurrent copying GC freed 93595(6022KB) AllocSpace objects, 2(40KB) LOS objects, 44% free, 7525KB/13MB, paused 12us,9us total 193.879ms
10-25 16:37:39.704  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:40.089  3141  4462 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 16:37:40.202  3141  4500 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 16:37:40.203  3141  4462 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 16:37:40.203  3141  4462 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 16:37:40.228  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:40.633  3141  3162 W .ghprotocol.app: Suspending all threads took: 6.453ms
10-25 16:37:40.634  3141  3162 I .ghprotocol.app: Background young concurrent copying GC freed 70188(6074KB) AllocSpace objects, 0(0B) LOS objects, 45% free, 7319KB/13MB, paused 11us,6.482ms total 16.745ms
10-25 16:37:40.728  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:41.426  3141  4462 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 16:37:41.750  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:42.774  3141  4462 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 16:37:42.937  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:42.949  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:42.962  3141  4561 D GhDiag  : relay dns -> 168B ok
10-25 16:37:43.078  3141  4562 D GhDiag  : relay dns -> 152B ok
10-25 16:37:43.085  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=60
10-25 16:37:43.165  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:43.165  3141  4462 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 16:37:43.167  3141  4566 D GhDiag  : relay tcp 34.153.x.x:443 -> socks5 ok
10-25 16:37:43.180  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=40
10-25 16:37:43.181  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=576
10-25 16:37:43.194  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=76
10-25 16:37:43.211  3141  4568 D GhDiag  : relay dns -> 168B ok
10-25 16:37:43.213  3141  4567 D GhDiag  : relay dns -> 264B ok
10-25 16:37:43.225  3141  4462 D GhDiag  : tun pkt proto=6 dst=34.153.x.x len=40
10-25 16:37:43.338  3141  4570 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 16:37:44.622  3141  3162 W .ghprotocol.app: Suspending all threads took: 14.447ms
10-25 16:37:44.683  3141  3162 I .ghprotocol.app: Background young concurrent copying GC freed 83557(7249KB) AllocSpace objects, 0(0B) LOS objects, 41% free, 7953KB/13MB, paused 2.794ms,14.515ms total 459.283ms

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
