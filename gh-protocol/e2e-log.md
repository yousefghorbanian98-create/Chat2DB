## gh-protocol E2E log — 2026-10-25T18:54:31Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T18:52:43Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 18:47 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 18:53 .
drwxr-xr-x 3 runner runner 4096 Oct 25 18:53 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 18:53 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 18:53 gh_test.ini

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
ERROR        | Unable to connect to adb daemon on port: 5037
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3182
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
WARNING: cannnot unmap ptr 0x7f9ba1601000 as it is in the protected range from 0x7f9aa1600000 to 0x7f9ba1800000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Successfully initialized netsim WiFi
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 38363 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 105
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 3182) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:36837 is gone due to Stream removed (CANCELLED)

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
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:packageDebugResources
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugResources
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugAssets
> Task :app:mergeDebugJniLibFolders
> Task :app:compressDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugNativeLibs
> Task :app:validateSigningDebug

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/ui/HomeViewModel.kt:539:17 Condition is always 'true'.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792954172929.json

BUILD SUCCESSFUL in 2m 56s
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
emulator can reach raw.githubusercontent.com after ~8s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2735)
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
    inet6 fe80::9118:4c85:5bc3:1fef/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.112.4): 56(84) bytes.

--- 140.82.112.4 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
--------- beginning of main
10-25 18:54:12.582  2735  2735 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 18:54:12.582  2735  2735 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 18:54:14.052  2735  2735 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 18:54:14.110  2735  2735 D GhDiag  : connect: config written bytes=5151 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 18:54:14.281  2735  2735 D GhDiag  : connect: core.start=true 
10-25 18:54:22.016  2735  2735 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 18:54:22.102  2735  2735 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@fd2baf6} — relay loop started
10-25 18:54:22.948  2735  4105 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 18:54:23.045  2735  2988 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (454ms)
10-25 18:54:23.091  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 18:54:23.402  2735  4105 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 18:54:23.529  2735  4150 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 18:54:23.529  2735  4105 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 18:54:23.530  2735  4105 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 18:54:23.608  2735  4141 D GhDiag  : relay dns -> 178B ok
10-25 18:54:24.402  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 18:54:24.413  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=893
10-25 18:54:24.698  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 18:54:25.302  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=893
10-25 18:54:25.595  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 18:54:25.758  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=115
10-25 18:54:25.758  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1274
10-25 18:54:25.759  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=156
10-25 18:54:25.805  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=115
10-25 18:54:25.890  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 18:54:25.899  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1274
10-25 18:54:25.946  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1278
10-25 18:54:26.072  2735  4105 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 18:54:26.090  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=156
10-25 18:54:26.193  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 18:54:26.247  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1278
10-25 18:54:26.473  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=115
10-25 18:54:26.474  2735  4105 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=60
10-25 18:54:26.489  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 18:54:26.499  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=57
10-25 18:54:26.520  2735  4335 D GhDiag  : relay dns -> 164B ok
10-25 18:54:26.582  2735  4358 D GhDiag  : relay dns -> 160B ok
10-25 18:54:26.604  2735  4364 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 18:54:26.654  2735  4372 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 18:54:12.582  2735  2735 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 18:54:12.582  2735  2735 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 18:54:14.052  2735  2735 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 18:54:14.110  2735  2735 D GhDiag  : connect: config written bytes=5151 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 18:54:14.281  2735  2735 D GhDiag  : connect: core.start=true 
10-25 18:54:22.016  2735  2735 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 18:54:22.102  2735  2735 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@fd2baf6} — relay loop started
10-25 18:54:22.948  2735  4105 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 18:54:23.045  2735  2988 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (454ms)
10-25 18:54:23.091  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 18:54:23.402  2735  4105 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 18:54:23.529  2735  4150 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 18:54:23.529  2735  4105 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 18:54:23.530  2735  4105 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 18:54:23.608  2735  4141 D GhDiag  : relay dns -> 178B ok
10-25 18:54:24.402  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 18:54:24.413  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=893
10-25 18:54:24.698  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 18:54:25.302  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=893
10-25 18:54:25.595  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 18:54:25.758  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=115
10-25 18:54:25.758  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1274
10-25 18:54:25.759  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=156
10-25 18:54:25.805  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=115
10-25 18:54:25.890  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 18:54:25.899  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1274
10-25 18:54:25.946  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1278
10-25 18:54:26.072  2735  4105 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 18:54:26.090  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=156
10-25 18:54:26.193  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 18:54:26.247  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1278
10-25 18:54:26.473  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=115
10-25 18:54:26.474  2735  4105 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=60
10-25 18:54:26.489  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 18:54:26.499  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=57
10-25 18:54:26.520  2735  4335 D GhDiag  : relay dns -> 164B ok
10-25 18:54:26.582  2735  4358 D GhDiag  : relay dns -> 160B ok
10-25 18:54:26.604  2735  4364 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 18:54:26.654  2735  4372 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
kId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:54:03.416   518   536 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=1 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{b6fe11e Task{7bcf819 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0xcb5e1a0 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{32777cc Task{d8c2012 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0x87e396c sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{null m=TO_FRONT f=IS_WALLPAPER leash=Surface(name=WallpaperWindowToken{925fc49 token=android.os.Binder@ee654aa})/@0x2f78aa3 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:54:03.417  2735  2735 W ziparchive: Unable to open '/data/app/~~CujqVhA2XnPtdr6KjYpBlA==/com.ghprotocol.app-CiyvX-lkRl6dRODXmEPqrA==/base.dm': No such file or directory
10-25 18:54:03.417  2735  2735 W ziparchive: Unable to open '/data/app/~~CujqVhA2XnPtdr6KjYpBlA==/com.ghprotocol.app-CiyvX-lkRl6dRODXmEPqrA==/base.dm': No such file or directory
10-25 18:54:04.079   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{63b4c6 com.google.android.youtube/10139} BLOCKED
10-25 18:54:04.079   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{2ac7c87 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 18:54:04.079   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{8cc57b4 com.google.android.as/10126} BLOCKED
10-25 18:54:04.079   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{af25fdd com.google.android.gm/10146} BLOCKED
10-25 18:54:04.080   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{4565752 com.google.android.devicelockcontroller/10170} BLOCKED
10-25 18:54:04.080   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{2ca5a23 com.google.android.contacts/10154} BLOCKED
10-25 18:54:04.080   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{1b13b20 com.google.android.partnersetup/10124} BLOCKED
10-25 18:54:04.080   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{33a1cd9 com.google.android.apps.youtube.music/10156} BLOCKED
10-25 18:54:04.080   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{d5e969e com.google.android.cellbroadcastreceiver/10180} BLOCKED
10-25 18:54:04.080   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{f5e757f com.google.android.inputmethod.latin/10142} BLOCKED
10-25 18:54:04.251  2735  2735 D nativeloader: Configuring clns-6 for other apk /data/app/~~CujqVhA2XnPtdr6KjYpBlA==/com.ghprotocol.app-CiyvX-lkRl6dRODXmEPqrA==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~CujqVhA2XnPtdr6KjYpBlA==/com.ghprotocol.app-CiyvX-lkRl6dRODXmEPqrA==/lib/x86_64:/data/app/~~CujqVhA2XnPtdr6KjYpBlA==/com.ghprotocol.app-CiyvX-lkRl6dRODXmEPqrA==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 18:54:04.288  2735  2735 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 18:54:04.288  2735  2735 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 18:54:05.619  2735  2735 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 18:54:05.619  2735  2735 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 18:54:05.619  2735  2735 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 18:54:05.619  2735  2735 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 18:54:05.619  2735  2735 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 18:54:05.619  2735  2735 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 18:54:05.619  2735  2735 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 18:54:06.270   518  1899 D CoreBackPreview: Window{a18515d u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@a6f4c62, mPriority=0, mIsAnimationCallback=false}
10-25 18:54:06.303  1089  1153 I Launcher.IconCache: Database bulk icon loading failed, using fallback bulk icon loading for: ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 18:54:07.929   518   536 W ziparchive: Unable to open '/data/app/~~CujqVhA2XnPtdr6KjYpBlA==/com.ghprotocol.app-CiyvX-lkRl6dRODXmEPqrA==/base.dm': No such file or directory
10-25 18:54:07.929   518   536 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +5s120ms
10-25 18:54:08.323   518   750 W InputManager-JNI: Input channel object '2c1f33b Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 18:54:08.324   518  1898 D CoreBackPreview: Window{2c1f33b u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-25 18:54:10.203   518   620 I InputDispatcher: a18515d com.ghprotocol.app/com.ghprotocol.app.MainActivity (server) spent 2347ms processing FocusEvent(hasFocus=true)
10-25 18:54:10.317   518  1724 I ImeTracker: com.ghprotocol.app:4b353e9f: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 18:54:10.317   518  1724 I ImeTracker: com.ghprotocol.app:4b353e9f: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 18:54:10.374  1535  1535 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 18:54:10.648  2735  3262 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 18:54:11.636   518  1001 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 18:54:11.637   839   873 V WindowManagerShell: Transition requested: android.os.BinderProxy@15bb383 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=50689 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@f0f8900} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{b5b8539 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:54:11.943  3353  3353 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 18:54:11.978  3353  3353 I AndroidRuntime: Using default boot image
10-25 18:54:11.978  3353  3353 I AndroidRuntime: Leaving lock profiling enabled
10-25 18:54:12.241  1610  1610 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 18:54:12.241  1610  1610 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 18:54:12.244  1610  3382 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 18:54:12.244  1610  3382 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 18:54:12.255  3353  3353 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 18:54:12.582  2735  2735 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 18:54:12.582  2735  2735 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 18:54:13.170  3464  3464 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:54:13.170  3464  3464 W libxraycore.so: type=1400 audit(0.0:19): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:54:13.170  3464  3464 W libxraycore.so: type=1400 audit(0.0:20): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:54:13.170  3464  3464 W libxraycore.so: type=1400 audit(0.0:21): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:54:13.321  3353  3353 D AndroidRuntime: Shutting down VM
10-25 18:54:14.052  2735  2735 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 18:54:14.110  2735  2735 D GhDiag  : connect: config written bytes=5151 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 18:54:14.118  3518  3518 W libxraycore.so: type=1400 audit(0.0:22): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:54:14.118  3518  3518 W libxraycore.so: type=1400 audit(0.0:23): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:54:14.118  3518  3518 W libxraycore.so: type=1400 audit(0.0:24): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:54:14.118  3518  3518 W libxraycore.so: type=1400 audit(0.0:25): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:54:14.281  2735  2735 D GhDiag  : connect: core.start=true 
10-25 18:54:14.386  3529  3529 W libxraycore.so: type=1400 audit(0.0:26): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 18:54:14.426   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{83eeb90 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 18:54:14.426   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{ff05c89 com.google.android.gm/10146} BLOCKED
10-25 18:54:14.426   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{7f548e com.google.android.dialer/10128} BLOCKED
10-25 18:54:14.427   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{5ce74af com.google.android.contacts/10154} BLOCKED
10-25 18:54:14.427   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{ecf30bc com.google.android.apps.youtube.music/10156} BLOCKED
10-25 18:54:14.580   518   825 D CoreBackPreview: Window{f80f6a2 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@db0f352, mPriority=0, mIsAnimationCallback=false}
10-25 18:54:15.390  3529  3529 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=54728 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 18:54:15.659   839   873 V WindowManagerShell: onTransitionReady android.os.BinderProxy@15bb383: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{1bf9fcd u0 com.ghprotocol.app/.MainActivity)/@0x376d7e8 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{9d57b60 u0 com.ghprotocol.app/.MainActivity)/@0x4d2ce01 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:54:15.669   839   873 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{1bf9fcd u0 com.ghprotocol.app/.MainActivity)/@0x376d7e8 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{9d57b60 u0 com.ghprotocol.app/.MainActivity)/@0x4d2ce01 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:54:15.670   839   873 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{1bf9fcd u0 com.ghprotocol.app/.MainActivity)/@0x376d7e8 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{9d57b60 u0 com.ghprotocol.app/.MainActivity)/@0x4d2ce01 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:54:15.803   518   536 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +4s36ms
10-25 18:54:15.803   518   536 V WindowManager: Sent Transition #7 createdAt=10-25 18:54:11.634 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=50689 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{b6fe11e Task{7bcf819 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{f65b418 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:54:15.803   518   536 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{1bf9fcd u0 com.ghprotocol.app/.MainActivity)/@0x12532f6 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{9d57b60 u0 com.ghprotocol.app/.MainActivity)/@0xdb29391 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 18:54:16.189   839   873 V WindowManagerShell: Transition requested: android.os.BinderProxy@d33f88a TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=54908 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@9970efb} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{d040b18 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:54:16.281   518  1722 W ProcessStats: Tracking association SourceState{611f225 com.ghprotocol.app/10192 BTop #1519} whose proc state 2 is better than process ProcessState{ae6f5fc com.google.android.gms.persistent/10131 pkg=com.google.android.gms} proc state 4 (5527 skipped)
10-25 18:54:16.379   518   539 W ActivityTaskManager: Activity top resumed state loss timeout for ActivityRecord{1bf9fcd u0 com.ghprotocol.app/.MainActivity t8}
10-25 18:54:16.380   518   539 W ActivityTaskManager: Activity pause timeout for ActivityRecord{1bf9fcd u0 com.ghprotocol.app/.MainActivity t8}
10-25 18:54:17.220   518  2025 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 18:54:17.222   518  2025 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 18:54:17.222   518  2025 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 18:54:18.119   518   536 V WindowManager: Sent Transition #8 createdAt=10-25 18:54:15.828 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=54908 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{b6fe11e Task{7bcf819 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{5c18f5b com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 18:54:18.643  3789  3789 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 18:54:18.651  3789  3789 I AndroidRuntime: Using default boot image
10-25 18:54:18.651  3789  3789 I AndroidRuntime: Leaving lock profiling enabled
10-25 18:54:18.774  3789  3789 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 18:54:19.762   518  2026 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{97acd3d com.google.android.gm/10146} BLOCKED
10-25 18:54:20.272  3789  3789 D AndroidRuntime: Shutting down VM
10-25 18:54:20.924   518  1849 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{4441cd8 com.google.android.settings.intelligence/10118} BLOCKED
10-25 18:54:20.925   518  1849 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{8da4831 com.google.android.settings.intelligence/10118} BLOCKED
10-25 18:54:21.639   518  2020 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 18:54:21.997   518   589 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 18:54:22.016  2735  2735 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 18:54:22.101   518  1722 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 18:54:22.102  2735  2735 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@fd2baf6} — relay loop started
10-25 18:54:22.311   518   532 I ImeTracker: com.ghprotocol.app:4bc93686: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 18:54:22.311   518   532 I ImeTracker: com.ghprotocol.app:4bc93686: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 18:54:22.400  1535  1535 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 18:54:22.948  2735  4105 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 18:54:23.045  2735  2988 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (454ms)
10-25 18:54:23.091  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 18:54:23.269  2735  2743 W .ghprotocol.app: Suspending all threads took: 6.910ms
10-25 18:54:23.277  2735  2743 I .ghprotocol.app: Background young concurrent copying GC freed 69685(4239KB) AllocSpace objects, 7(140KB) LOS objects, 33% free, 7792KB/11MB, paused 13us,7.081ms total 327.419ms
10-25 18:54:23.402  2735  4105 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 18:54:23.529  2735  4150 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 18:54:23.529  2735  4105 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 18:54:23.530  2735  4105 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 18:54:23.608  2735  4141 D GhDiag  : relay dns -> 178B ok
10-25 18:54:24.108  2735  2743 I .ghprotocol.app: Background concurrent copying GC freed 58824(4247KB) AllocSpace objects, 11(240KB) LOS objects, 49% free, 7754KB/15MB, paused 31us,8us total 327.652ms
10-25 18:54:24.177  2735  2742 I .ghprotocol.app: Compiler allocated 4257KB to compile void com.ghprotocol.app.ui.MotionComponentsKt.DefyxHeaderSection(com.ghprotocol.app.ui.ConnectPhase, java.lang.Integer, boolean, java.lang.String, java.lang.String, com.ghprotocol.app.core.TunnelTelemetry, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-25 18:54:24.402  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 18:54:24.413  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=893
10-25 18:54:24.698  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 18:54:24.861   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{e99a67b com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 18:54:24.861   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{6478c98 com.android.camera2/10144} BLOCKED
10-25 18:54:24.861   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{edd5cf1 com.google.android.gm/10146} BLOCKED
10-25 18:54:24.861   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{9f830d6 com.google.android.devicelockcontroller/10170} BLOCKED
10-25 18:54:24.862   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{9122f57 com.google.android.rkpdapp/10181} BLOCKED
10-25 18:54:24.862   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{b74da44 com.google.android.settings.intelligence/10118} BLOCKED
10-25 18:54:24.863   518   571 I AppsFilter: interaction: PackageSetting{1d5baa1 com.ghprotocol.app/10192} -> PackageSetting{cb0b8e4 com.google.android.projection.gearhead/10123} BLOCKED
10-25 18:54:25.302  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=893
10-25 18:54:25.595  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 18:54:25.758  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=115
10-25 18:54:25.758  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1274
10-25 18:54:25.759  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=156
10-25 18:54:25.805  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=115
10-25 18:54:25.890  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 18:54:25.899  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1274
10-25 18:54:25.946  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1278
10-25 18:54:26.072  2735  4105 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 18:54:26.090  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=156
10-25 18:54:26.193  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=1278
10-25 18:54:26.247  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=1278
10-25 18:54:26.473  2735  4105 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=115
10-25 18:54:26.474  2735  4105 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=60
10-25 18:54:26.489  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 18:54:26.499  2735  4105 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=57
10-25 18:54:26.520  2735  4335 D GhDiag  : relay dns -> 164B ok
10-25 18:54:26.582  2735  4358 D GhDiag  : relay dns -> 160B ok
10-25 18:54:26.604  2735  4364 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 18:54:26.654  2735  4372 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 18:54:26.688  1398  3746 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 18:54:26.946  1454  3442 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 18:54:27.788  2735  2743 I .ghprotocol.app: Background young concurrent copying GC freed 97471(8004KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 7779KB/15MB, paused 10.449ms,21us total 47.317ms

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
