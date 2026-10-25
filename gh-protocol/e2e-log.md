## gh-protocol E2E log — 2026-10-25T15:58:15Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T15:56:58Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 15:53 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 15:57 .
drwxr-xr-x 3 runner runner 4096 Oct 25 15:57 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 15:57 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 15:57 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3055
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
WARNING: cannnot unmap ptr 0x7f1653001000 as it is in the protected range from 0x7f1553000000 to 0x7f1653200000
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
INFO         | Boot completed in 26957 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 130
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 3055) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 1 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:42627 is gone due to Stream removed (CANCELLED)

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
> Task :app:generateDebugBuildConfig
> Task :app:createDebugCompatibleScreenManifests
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:packageDebugResources
> Task :app:parseDebugLocalResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugNativeLibs
> Task :app:mergeDebugResources
> Task :app:compressDebugAssets

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:mergeLibDexDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:validateSigningDebug
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792943683579.json

BUILD SUCCESSFUL in 1m 47s
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
emulator can reach raw.githubusercontent.com after ~4s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2825)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tunnel up after ~4s (xray pid + :10808 listener)
== wait for VpnService establish (consent result) ==
tapped VPN consent at: 894 1519 (iter vpn-1)
vpn established after ~6s
18: tun0: <POINTOPOINT,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 10.8.0.2/24 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fd00:1::1/128 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::3737:78b5:d1c5:5cd3/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (20.29.134.23): 56(84) bytes.

--- 20.29.134.23 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
--------- beginning of main
10-25 15:58:02.983  2825  2825 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 15:58:02.984  2825  2825 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 15:58:03.244  2825  2825 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 15:58:03.271  2825  2825 D GhDiag  : connect: config written bytes=5112 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 15:58:03.408  2825  2825 D GhDiag  : connect: core.start=true 
10-25 15:58:08.688  2825  2825 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 15:58:08.746  2825  2825 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@b522086} — relay loop started
10-25 15:58:09.073  2825  3064 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (111ms)
10-25 15:58:09.338  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:09.419  2825  4456 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:58:09.419  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:09.423  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:09.459  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 15:58:09.627  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:09.724  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:09.991  2825  4456 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 15:58:09.994  2825  4456 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 15:58:09.994  2825  4456 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 15:58:09.996  2825  4493 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 15:58:10.004  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:58:10.035  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:58:10.055  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:10.327  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:10.439  2825  4456 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:58:10.654  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:58:10.659  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:58:10.921  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:11.308  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:58:11.310  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:58:11.427  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=61
10-25 15:58:11.427  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=61
10-25 15:58:11.462  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:58:11.464  2825  4456 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:58:11.480  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 15:58:02.983  2825  2825 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 15:58:02.984  2825  2825 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 15:58:03.244  2825  2825 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 15:58:03.271  2825  2825 D GhDiag  : connect: config written bytes=5112 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 15:58:03.408  2825  2825 D GhDiag  : connect: core.start=true 
10-25 15:58:08.688  2825  2825 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 15:58:08.746  2825  2825 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@b522086} — relay loop started
10-25 15:58:09.073  2825  3064 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (111ms)
10-25 15:58:09.338  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:09.419  2825  4456 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:58:09.419  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:09.423  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:09.459  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 15:58:09.627  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:09.724  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:09.991  2825  4456 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 15:58:09.994  2825  4456 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 15:58:09.994  2825  4456 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 15:58:09.996  2825  4493 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 15:58:10.004  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:58:10.035  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:58:10.055  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:10.327  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:10.439  2825  4456 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:58:10.654  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:58:10.659  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:58:10.921  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:11.308  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:58:11.310  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:58:11.427  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=61
10-25 15:58:11.427  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=61
10-25 15:58:11.462  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:58:11.464  2825  4456 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:58:11.480  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:57:54.672   520  2518 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 15:57:54.768   520   943 D CoreBackPreview: Window{2d06598 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@76f016b, mPriority=0, mIsAnimationCallback=false}
10-25 15:57:54.787   520   548 I ActivityManager: Start proc 2825:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 15:57:55.118   520   537 V WindowManager: Sent Transition #6 createdAt=10-25 15:57:54.539 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=30932 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{6aa68c5 Task{1323a25 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{fd8d21a com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:57:55.118   520   537 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{6aa68c5 Task{1323a25 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0xbb112f sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{971914b Task{b937e6a #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0x7e4b380 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{null m=TO_FRONT f=IS_WALLPAPER leash=Surface(name=WallpaperWindowToken{825240f token=android.os.Binder@c0fa56e})/@0xc02930e sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:57:55.713  1082  1140 I Launcher.IconCache: Database bulk icon loading failed, using fallback bulk icon loading for: ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 15:57:55.798  2825  2825 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 15:57:55.835  2825  2825 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 15:57:55.835  2825  2825 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 15:57:55.835  2825  2825 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 15:57:55.980  2825  2825 W ziparchive: Unable to open '/data/app/~~uclD8X7sLP4p5H0uM6CT2g==/com.ghprotocol.app-u4sn_0NNSEC-NSJI--F5Iw==/base.dm': No such file or directory
10-25 15:57:55.980  2825  2825 W ziparchive: Unable to open '/data/app/~~uclD8X7sLP4p5H0uM6CT2g==/com.ghprotocol.app-u4sn_0NNSEC-NSJI--F5Iw==/base.dm': No such file or directory
10-25 15:57:56.151   520   797 I SdkSandboxManager: No SDKs used. Skipping SDK data reconcilation for CallingInfo{mUid=10192, mPackageName='com.ghprotocol.app, mAppProcessToken='null'}
10-25 15:57:56.351  2825  2825 D nativeloader: Configuring clns-6 for other apk /data/app/~~uclD8X7sLP4p5H0uM6CT2g==/com.ghprotocol.app-u4sn_0NNSEC-NSJI--F5Iw==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~uclD8X7sLP4p5H0uM6CT2g==/com.ghprotocol.app-u4sn_0NNSEC-NSJI--F5Iw==/lib/x86_64:/data/app/~~uclD8X7sLP4p5H0uM6CT2g==/com.ghprotocol.app-u4sn_0NNSEC-NSJI--F5Iw==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 15:57:56.381  2825  2825 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 15:57:56.381  2825  2825 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 15:57:56.715   520   533 W InputManager-JNI: Input channel object '1faf987 com.ghprotocol.app/com.ghprotocol.app.MainActivity (client)' was disposed without first being removed with the input manager!
10-25 15:57:56.910   520  1753 D CoreBackPreview: Window{6556c76 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@5ebb888, mPriority=0, mIsAnimationCallback=false}
10-25 15:57:56.922   831   831 I SafetyLabelChangedBroadcastReceiver: received broadcast packageName: com.ghprotocol.app, current user: UserHandle{0}, packageChangeEvent: NEW_INSTALL, intent user: UserHandle{0}
10-25 15:57:57.086  2825  2825 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 15:57:57.086  2825  2825 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 15:57:57.086  2825  2825 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 15:57:57.086  2825  2825 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 15:57:57.086  2825  2825 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 15:57:57.086  2825  2825 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 15:57:57.086  2825  2825 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 15:57:57.477  1039  1039 D CarrierSvcBindHelper: onPackageAdded: com.ghprotocol.app
10-25 15:57:57.510  1039  1321 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 15:57:57.553  1039  1039 D CarrierSvcBindHelper: onPackageModified: com.ghprotocol.app
10-25 15:57:57.597  1039  1321 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 15:57:58.128   520   945 I WindowManager: finishDrawing of relaunch: Window{6556c76 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity} 2048ms
10-25 15:57:58.133   520   537 W ziparchive: Unable to open '/data/app/~~uclD8X7sLP4p5H0uM6CT2g==/com.ghprotocol.app-u4sn_0NNSEC-NSJI--F5Iw==/base.dm': No such file or directory
10-25 15:57:58.135   520   537 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s633ms
10-25 15:57:58.177   520   744 W InputManager-JNI: Input channel object '2d06598 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 15:57:58.386   520   587 I ImeTracker: com.ghprotocol.app:6ca4e905: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 15:57:58.387   520   587 I ImeTracker: com.ghprotocol.app:6ca4e905: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 15:57:58.400  1493  1493 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 15:57:58.647   520  1759 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{d1b4c22 com.google.android.gm/10141} BLOCKED
10-25 15:58:00.207   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{ffe9cea com.google.android.youtube/10139} BLOCKED
10-25 15:58:00.208   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{a344bdb com.google.android.googlequicksearchbox/10131} BLOCKED
10-25 15:58:00.208   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{dc33678 com.android.camera2/10146} BLOCKED
10-25 15:58:00.208   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{f86f151 com.google.android.as/10125} BLOCKED
10-25 15:58:00.208   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{fa19db6 com.google.android.devicelockcontroller/10181} BLOCKED
10-25 15:58:00.209   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{6a1cab7 com.google.android.dialer/10128} BLOCKED
10-25 15:58:00.209   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{f314224 com.google.android.contacts/10155} BLOCKED
10-25 15:58:00.209   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{5f8518d com.google.android.partnersetup/10124} BLOCKED
10-25 15:58:00.209   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{3a1df42 com.google.android.apps.youtube.music/10156} BLOCKED
10-25 15:58:00.209   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{cfe5b53 com.google.android.inputmethod.latin/10142} BLOCKED
10-25 15:58:02.045   520  2567 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{d49fc93 com.google.android.settings.intelligence/10117} BLOCKED
10-25 15:58:02.081  2825  3831 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 15:58:02.866   520  1753 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 15:58:02.866   829   859 V WindowManagerShell: Transition requested: android.os.BinderProxy@74dc9e TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=39076 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@d2e437f} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{87d9f4c com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:58:02.983  2825  2825 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 15:58:02.984  2825  2825 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 15:58:02.989  3971  3971 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 15:58:02.993  3971  3971 I AndroidRuntime: Using default boot image
10-25 15:58:02.993  3971  3971 I AndroidRuntime: Leaving lock profiling enabled
10-25 15:58:03.055  3991  3991 W libxraycore.so: type=1400 audit(0.0:15): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 15:58:03.055  3991  3991 W libxraycore.so: type=1400 audit(0.0:16): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 15:58:03.055  3991  3991 W libxraycore.so: type=1400 audit(0.0:17): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 15:58:03.055  3991  3991 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 15:58:03.130  3971  3971 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 15:58:03.244  2825  2825 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 15:58:03.271  2825  2825 D GhDiag  : connect: config written bytes=5112 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 15:58:03.408  2825  2825 D GhDiag  : connect: core.start=true 
10-25 15:58:03.417   520   744 D CoreBackPreview: Window{a804d7f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@ac33232, mPriority=0, mIsAnimationCallback=false}
10-25 15:58:04.203  3971  3971 D AndroidRuntime: Shutting down VM
10-25 15:58:04.287  4052  4052 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=56707 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 15:58:04.491   520   537 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s682ms
10-25 15:58:04.492   829   859 V WindowManagerShell: onTransitionReady android.os.BinderProxy@74dc9e: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{284b4a u0 com.ghprotocol.app/.MainActivity)/@0xbae8be4 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{89832f0 u0 com.ghprotocol.app/.MainActivity)/@0xe49384d sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:58:04.493   829   859 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{284b4a u0 com.ghprotocol.app/.MainActivity)/@0xbae8be4 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{89832f0 u0 com.ghprotocol.app/.MainActivity)/@0xe49384d sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:58:04.494   520   537 V WindowManager: Sent Transition #7 createdAt=10-25 15:58:02.802 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=39076 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{6aa68c5 Task{1323a25 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{332deb4 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:58:04.494   829   859 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{284b4a u0 com.ghprotocol.app/.MainActivity)/@0xbae8be4 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{89832f0 u0 com.ghprotocol.app/.MainActivity)/@0xe49384d sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:58:04.495   520   537 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{284b4a u0 com.ghprotocol.app/.MainActivity)/@0x1df23c6 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{89832f0 u0 com.ghprotocol.app/.MainActivity)/@0xd6d85a1 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 15:58:04.947   829   859 V WindowManagerShell: Transition requested: android.os.BinderProxy@c439426 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=40872 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@b4dd867} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{ebeb614 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:58:05.066   520  1758 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 15:58:05.074   520  1758 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 15:58:05.074   520  1758 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 15:58:05.088   520  2501 I ImeTracker: com.ghprotocol.app:ddf0757c: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 15:58:05.088   520  2501 I ImeTracker: com.ghprotocol.app:ddf0757c: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 15:58:05.090  1493  1493 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 15:58:05.796   520   537 V WindowManager: Sent Transition #8 createdAt=10-25 15:58:04.553 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=40872 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{6aa68c5 Task{1323a25 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{62a2c99 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 15:58:06.134  4297  4297 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 15:58:06.142  4297  4297 I AndroidRuntime: Using default boot image
10-25 15:58:06.142  4297  4297 I AndroidRuntime: Leaving lock profiling enabled
10-25 15:58:06.210  4297  4297 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 15:58:06.387  2825  2858 W .ghprotocol.app: Cleared Reference was only reachable from finalizer (only reported once)
10-25 15:58:06.393  2825  2858 I .ghprotocol.app: Background concurrent copying GC freed 119850(6046KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6725KB/13MB, paused 22us,8us total 356.240ms
10-25 15:58:07.304  4297  4297 D AndroidRuntime: Shutting down VM
10-25 15:58:07.692  1587  1587 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 15:58:07.716  1587  1587 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 15:58:07.716  1587  2914 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 15:58:07.716  1587  2914 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 15:58:08.539   520  2567 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 15:58:08.686   520  2749 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 15:58:08.688  2825  2825 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 15:58:08.741   520  2749 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 15:58:08.746  2825  2825 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@b522086} — relay loop started
10-25 15:58:08.769   520  1086 I ImeTracker: com.ghprotocol.app:b96ebfdf: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 15:58:08.769   520  1086 I ImeTracker: com.ghprotocol.app:b96ebfdf: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 15:58:08.779  1493  1493 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 15:58:09.073  2825  3064 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (111ms)
10-25 15:58:09.338  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:09.419  2825  4456 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:58:09.419  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:09.423  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:09.459  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 15:58:09.501  2825  2857 I .ghprotocol.app: Compiler allocated 4108KB to compile void com.ghprotocol.app.ui.HomeScreenKt.WorldClassConnectHub(com.ghprotocol.app.ui.HomeUiState, com.ghprotocol.app.ui.HomeViewModel, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, kotlin.jvm.functions.Function0, androidx.compose.ui.Modifier, androidx.compose.runtime.Composer, int, int)
10-25 15:58:09.627  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:09.724  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:09.991  2825  4456 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 15:58:09.994  2825  4456 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 15:58:09.994  2825  4456 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 15:58:09.996  2825  4493 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 15:58:10.004  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:58:10.035  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:58:10.055  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:10.303   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{2f7ce5 com.google.android.googlequicksearchbox/10131} BLOCKED
10-25 15:58:10.304   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{a6423ba com.google.android.apps.messaging/10130} BLOCKED
10-25 15:58:10.304   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{b62126b com.google.android.gm/10141} BLOCKED
10-25 15:58:10.304   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{420a1c8 com.google.android.devicelockcontroller/10181} BLOCKED
10-25 15:58:10.304   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{be00261 com.google.android.rkpdapp/10186} BLOCKED
10-25 15:58:10.304   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{720c186 com.google.android.settings.intelligence/10117} BLOCKED
10-25 15:58:10.304   520   571 I AppsFilter: interaction: PackageSetting{7b1e5ed com.ghprotocol.app/10192} -> PackageSetting{62f2dfb com.google.android.projection.gearhead/10123} BLOCKED
10-25 15:58:10.327  2825  4456 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 15:58:10.439  2825  4456 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:58:10.654  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:58:10.659  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 15:58:10.921  2825  4456 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 15:58:10.952  1402  3946 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 15:58:10.957  1449  4168 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 15:58:11.308  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:58:11.310  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 15:58:11.427  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=61
10-25 15:58:11.427  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=61
10-25 15:58:11.462  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68
10-25 15:58:11.464  2825  4456 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 15:58:11.480  2825  4456 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=68

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
