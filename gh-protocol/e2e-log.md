## gh-protocol E2E log — 2026-10-25T09:33:43Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T09:31:57Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 09:28 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 09:32 .
drwxr-xr-x 3 runner runner 4096 Oct 25 09:32 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 09:32 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 09:32 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 3077
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
WARNING: cannnot unmap ptr 0x7f81cfc01000 as it is in the protected range from 0x7f80cfc00000 to 0x7f81cfe00000
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
INFO         | Boot completed in 37981 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 86
ERROR        | Failed to bind to texture: invalid color buffer.
ERROR        | Failed to find ColorBuffer: 115
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 3077) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 1 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:44809 is gone due to Stream removed (CANCELLED)

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
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
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
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugAssets
> Task :app:mergeDebugResources
> Task :app:parseDebugLocalResources
> Task :app:mergeExtDexDebug
> Task :app:compressDebugAssets
> Task :app:mergeLibDexDebug
> Task :app:processDebugResources
> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792920550540.json

BUILD SUCCESSFUL in 2m 37s
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
app up (try 1, pid 2758)
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
    inet6 fe80::d323:b102:34cf:c508/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.114.3): 56(84) bytes.

--- 140.82.114.3 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
10-25 09:33:26.394  2758  2758 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 09:33:26.438  2758  2758 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 09:33:26.499  2758  2758 D GhDiag  : connect: core.start=true 
10-25 09:33:33.165  2758  2758 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 09:33:33.206  2758  2758 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@b539f8e} — relay loop started
10-25 09:33:33.533  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=40
10-25 09:33:33.534  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=197
10-25 09:33:33.580  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 09:33:33.611  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 09:33:33.683  2758  4023 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 09:33:33.766  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 09:33:33.809  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 09:33:33.812  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=40
10-25 09:33:33.815  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 09:33:33.844  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 09:33:34.160  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=197
10-25 09:33:34.412  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.426  2758  4174 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 09:33:34.426  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 09:33:34.427  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 09:33:34.427  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.429  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.531  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.718  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 09:33:34.732  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.741  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 09:33:35.549  2758  4117 D GhDiag  : relay dns -> 274B ok
10-25 09:33:35.549  2758  4110 D GhDiag  : relay dns -> 178B ok
10-25 09:33:35.552  2758  4085 D GhDiag  : relay dns -> 269B ok
10-25 09:33:35.554  2758  4078 D GhDiag  : relay dns -> 173B ok
10-25 09:33:35.592  2758  4285 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.146  2758  4120 D GhDiag  : relay dns -> 45B ok
10-25 09:33:36.236  2758  4215 D GhDiag  : relay dns -> 260B ok
10-25 09:33:36.253  2758  4216 D GhDiag  : relay dns -> 164B ok
10-25 09:33:36.257  2758  4323 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.508  2758  4232 D GhDiag  : relay dns -> 273B ok
10-25 09:33:36.514  2758  4231 D GhDiag  : relay dns -> 177B ok
10-25 09:33:36.693  2758  4338 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.694  2758  4126 D GhDiag  : relay dns -> 29B ok
10-25 09:33:36.737  2758  4340 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.984  2758  4348 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:37.208  2758  4293 D GhDiag  : relay dns -> 44B ok
10-25 09:33:37.225  2758  4292 D GhDiag  : relay dns -> 112B ok
10-25 09:33:38.912  2758  4392 D GhDiag  : relay dns -> 160B ok
10-25 09:33:38.921  2758  4393 D GhDiag  : relay dns -> 256B ok
10-25 09:33:38.926  2758  4562 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 09:33:39.245  2758  4565 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:39.318  2758  4570 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
10-25 09:33:39.370  2758  4339 D GhDiag  : relay dns -> 29B ok
10-25 09:33:39.392  2758  4576 D GhDiag  : relay tcp 5.61.x.x:443 -> socks5 ok
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 09:33:26.085  2758  2758 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 09:33:26.085  2758  2758 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 09:33:26.394  2758  2758 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 09:33:26.438  2758  2758 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 09:33:26.499  2758  2758 D GhDiag  : connect: core.start=true 
10-25 09:33:33.165  2758  2758 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 09:33:33.206  2758  2758 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@b539f8e} — relay loop started
10-25 09:33:33.533  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=40
10-25 09:33:33.534  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=197
10-25 09:33:33.580  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 09:33:33.611  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 09:33:33.683  2758  4023 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 09:33:33.766  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 09:33:33.809  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 09:33:33.812  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=40
10-25 09:33:33.815  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 09:33:33.844  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 09:33:34.160  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=197
10-25 09:33:34.412  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.426  2758  4174 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 09:33:34.426  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 09:33:34.427  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 09:33:34.427  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.429  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.531  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.718  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 09:33:34.732  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.741  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 09:33:35.549  2758  4117 D GhDiag  : relay dns -> 274B ok
10-25 09:33:35.549  2758  4110 D GhDiag  : relay dns -> 178B ok
10-25 09:33:35.552  2758  4085 D GhDiag  : relay dns -> 269B ok
10-25 09:33:35.554  2758  4078 D GhDiag  : relay dns -> 173B ok
10-25 09:33:35.592  2758  4285 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.146  2758  4120 D GhDiag  : relay dns -> 45B ok
10-25 09:33:36.236  2758  4215 D GhDiag  : relay dns -> 260B ok
10-25 09:33:36.253  2758  4216 D GhDiag  : relay dns -> 164B ok
10-25 09:33:36.257  2758  4323 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.508  2758  4232 D GhDiag  : relay dns -> 273B ok
10-25 09:33:36.514  2758  4231 D GhDiag  : relay dns -> 177B ok
10-25 09:33:36.693  2758  4338 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.694  2758  4126 D GhDiag  : relay dns -> 29B ok
10-25 09:33:36.737  2758  4340 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.984  2758  4348 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:37.208  2758  4293 D GhDiag  : relay dns -> 44B ok
10-25 09:33:37.225  2758  4292 D GhDiag  : relay dns -> 112B ok
10-25 09:33:38.912  2758  4392 D GhDiag  : relay dns -> 160B ok
10-25 09:33:38.921  2758  4393 D GhDiag  : relay dns -> 256B ok
10-25 09:33:38.926  2758  4562 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 09:33:39.245  2758  4565 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:39.318  2758  4570 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
10-25 09:33:39.370  2758  4339 D GhDiag  : relay dns -> 29B ok
10-25 09:33:39.392  2758  4576 D GhDiag  : relay tcp 5.61.x.x:443 -> socks5 ok
10-25 09:33:39.925  2758  4538 D GhDiag  : relay dns -> 160B ok
10-25 09:33:39.944  2758  4539 D GhDiag  : relay dns -> 256B ok
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
16.833   519   586 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 09:33:17.064   519  2631 D CoreBackPreview: Window{e466f11 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@f3ef5d4, mPriority=0, mIsAnimationCallback=false}
10-25 09:33:17.710  2758  2758 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 09:33:17.725  2758  2758 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 09:33:17.725  2758  2758 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 09:33:17.725  2758  2758 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 09:33:17.735   519   547 I ActivityManager: Start proc 2758:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 09:33:17.879   519   536 V WindowManager: Sent Transition #6 createdAt=10-25 09:33:16.720 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=42899 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{1239ea4 Task{b601e3d #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{d58b40d com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 09:33:17.880   519   536 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{1239ea4 Task{b601e3d #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0x130caf8 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{4aecfc2 Task{cc5a425 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0xae7d633 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 09:33:18.651  2758  2758 W ziparchive: Unable to open '/data/app/~~aI46ralyaMKfdz94qRssOg==/com.ghprotocol.app-YXPCRW3UUjrxel7I59tMpA==/base.dm': No such file or directory
10-25 09:33:18.652  2758  2758 W ziparchive: Unable to open '/data/app/~~aI46ralyaMKfdz94qRssOg==/com.ghprotocol.app-YXPCRW3UUjrxel7I59tMpA==/base.dm': No such file or directory
10-25 09:33:19.344  2758  2758 D nativeloader: Configuring clns-6 for other apk /data/app/~~aI46ralyaMKfdz94qRssOg==/com.ghprotocol.app-YXPCRW3UUjrxel7I59tMpA==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~aI46ralyaMKfdz94qRssOg==/com.ghprotocol.app-YXPCRW3UUjrxel7I59tMpA==/lib/x86_64:/data/app/~~aI46ralyaMKfdz94qRssOg==/com.ghprotocol.app-YXPCRW3UUjrxel7I59tMpA==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 09:33:19.390  2758  2758 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 09:33:19.390  2758  2758 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 09:33:20.216   519   798 I SdkSandboxManager: No SDKs used. Skipping SDK data reconcilation for CallingInfo{mUid=10192, mPackageName='com.ghprotocol.app, mAppProcessToken='null'}
10-25 09:33:20.552   835   835 I SafetyLabelChangedBroadcastReceiver: received broadcast packageName: com.ghprotocol.app, current user: UserHandle{0}, packageChangeEvent: NEW_INSTALL, intent user: UserHandle{0}
10-25 09:33:20.960  2758  2758 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 09:33:20.960  2758  2758 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 09:33:20.960  2758  2758 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 09:33:20.974  2758  2758 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 09:33:20.974  2758  2758 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 09:33:20.974  2758  2758 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 09:33:20.974  2758  2758 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 09:33:21.200   519   991 D CoreBackPreview: Window{6768413 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@9e4b5ca, mPriority=0, mIsAnimationCallback=false}
10-25 09:33:21.591  1043  1043 D CarrierSvcBindHelper: onPackageAdded: com.ghprotocol.app
10-25 09:33:21.605  1043  1334 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 09:33:22.610   519  1641 I WindowManager: finishDrawing of relaunch: Window{6768413 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity} 2204ms
10-25 09:33:22.626   519   536 W ziparchive: Unable to open '/data/app/~~aI46ralyaMKfdz94qRssOg==/com.ghprotocol.app-YXPCRW3UUjrxel7I59tMpA==/base.dm': No such file or directory
10-25 09:33:22.631   519   536 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +5s978ms
10-25 09:33:22.673   519  2637 D CoreBackPreview: Window{6768413 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback null
10-25 09:33:22.673   519  1880 D CoreBackPreview: Window{e466f11 u0 Splash Screen com.ghprotocol.app}: Setting back callback null
10-25 09:33:22.673   519  2404 W InputManager-JNI: Input channel object '6768413 com.ghprotocol.app/com.ghprotocol.app.MainActivity (client)' was disposed without first being removed with the input manager!
10-25 09:33:22.684   519   532 W InputManager-JNI: Input channel object 'e466f11 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 09:33:23.136   519  1915 D CoreBackPreview: Window{9f4821f u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@b1ec0e7, mPriority=0, mIsAnimationCallback=false}
10-25 09:33:23.543   519  2401 I ImeTracker: com.ghprotocol.app:e3235d2e: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 09:33:23.543   519  2401 I ImeTracker: com.ghprotocol.app:e3235d2e: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 09:33:23.563  1555  1555 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 09:33:23.592  1043  1043 D CarrierSvcBindHelper: onPackageModified: com.ghprotocol.app
10-25 09:33:23.706  1043  1334 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 09:33:25.275   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{e050e56 com.google.android.youtube/10139} BLOCKED
10-25 09:33:25.276   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{f097ed7 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 09:33:25.276   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{cfab3c4 com.google.android.gm/10147} BLOCKED
10-25 09:33:25.276   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{71c72ad com.google.android.dialer/10128} BLOCKED
10-25 09:33:25.276   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{dbb9e2 com.google.android.contacts/10154} BLOCKED
10-25 09:33:25.276   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{6fd3173 com.google.android.apps.youtube.music/10156} BLOCKED
10-25 09:33:25.494   519  2578 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 09:33:25.495   828   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@5f992b TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=51588 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@ba18188} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{6bc721 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 09:33:25.781  3465  3465 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 09:33:25.793  3465  3465 I AndroidRuntime: Using default boot image
10-25 09:33:25.795  3465  3465 I AndroidRuntime: Leaving lock profiling enabled
10-25 09:33:26.067  3465  3465 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 09:33:26.085  2758  2758 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 09:33:26.085  2758  2758 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 09:33:26.152  3509  3509 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 09:33:26.152  3509  3509 W libxraycore.so: type=1400 audit(0.0:19): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 09:33:26.152  3509  3509 W libxraycore.so: type=1400 audit(0.0:20): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 09:33:26.152  3509  3509 W libxraycore.so: type=1400 audit(0.0:21): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 09:33:26.394  2758  2758 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 09:33:26.438  2758  2758 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 09:33:26.499  2758  2758 D GhDiag  : connect: core.start=true 
10-25 09:33:26.558   519  2630 D CoreBackPreview: Window{dbf6425 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@7aa9e80, mPriority=0, mIsAnimationCallback=false}
10-25 09:33:27.352  3465  3465 D AndroidRuntime: Shutting down VM
10-25 09:33:27.503   828   865 V WindowManagerShell: onTransitionReady android.os.BinderProxy@5f992b: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{a05d142 u0 com.ghprotocol.app/.MainActivity)/@0x72dd571 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{53a9394 u0 com.ghprotocol.app/.MainActivity)/@0xbf27f56 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 09:33:27.513   519   536 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +2s153ms
10-25 09:33:27.513   519   536 V WindowManager: Sent Transition #7 createdAt=10-25 09:33:25.360 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=51588 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{1239ea4 Task{b601e3d #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{7693204 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 09:33:27.513   828   865 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{a05d142 u0 com.ghprotocol.app/.MainActivity)/@0x72dd571 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{53a9394 u0 com.ghprotocol.app/.MainActivity)/@0xbf27f56 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 09:33:27.518   828   865 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{a05d142 u0 com.ghprotocol.app/.MainActivity)/@0x72dd571 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{53a9394 u0 com.ghprotocol.app/.MainActivity)/@0xbf27f56 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 09:33:27.525   519   536 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{a05d142 u0 com.ghprotocol.app/.MainActivity)/@0x5faedb1 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{53a9394 u0 com.ghprotocol.app/.MainActivity)/@0x391e858 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 09:33:27.915   828   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@44dfce1 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=53637 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@f476a06} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{a5a28c7 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 09:33:27.930  2758  3627 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 09:33:27.936  3535  3535 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=54168 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 09:33:27.984   519   991 I ImeTracker: com.ghprotocol.app:c5679ea5: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 09:33:27.985   519   991 I ImeTracker: com.ghprotocol.app:c5679ea5: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 09:33:27.999  1555  1555 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 09:33:28.062  2758  2773 W .ghprotocol.app: Cleared Reference was only reachable from finalizer (only reported once)
10-25 09:33:28.064  2758  2773 I .ghprotocol.app: Background concurrent copying GC freed 97971(5160KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6129KB/11MB, paused 27us,9us total 332.966ms
10-25 09:33:28.523   519  2637 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 09:33:28.528   519  2637 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 09:33:28.528   519  2637 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 09:33:29.102  3746  3746 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 09:33:29.107  3746  3746 I AndroidRuntime: Using default boot image
10-25 09:33:29.107  3746  3746 I AndroidRuntime: Leaving lock profiling enabled
10-25 09:33:29.299  3746  3746 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 09:33:29.579   519   536 V WindowManager: Sent Transition #8 createdAt=10-25 09:33:27.533 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=53637 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{1239ea4 Task{b601e3d #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{5dc0af5 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 09:33:31.305  3746  3746 D AndroidRuntime: Shutting down VM
10-25 09:33:31.701   519  2397 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{13b0562 com.google.android.gm/10147} BLOCKED
10-25 09:33:32.549   519   816 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 09:33:33.164   519   816 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 09:33:33.165  2758  2758 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 09:33:33.205   519  2401 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 09:33:33.206  2758  2758 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@b539f8e} — relay loop started
10-25 09:33:33.256   519   899 I ImeTracker: com.ghprotocol.app:1bdef4c4: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 09:33:33.256   519   899 I ImeTracker: com.ghprotocol.app:1bdef4c4: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 09:33:33.274  1555  1555 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 09:33:33.533  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=40
10-25 09:33:33.534  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=197
10-25 09:33:33.580  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 09:33:33.611  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=73
10-25 09:33:33.683  2758  4023 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 09:33:33.766  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 09:33:33.809  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 09:33:33.812  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=40
10-25 09:33:33.815  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 09:33:33.844  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=57
10-25 09:33:34.160  2758  4023 D GhDiag  : tun pkt proto=6 dst=5.106.x.x len=197
10-25 09:33:34.297   519  1167 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{f78e813 com.google.android.settings.intelligence/10118} BLOCKED
10-25 09:33:34.298   519  2402 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{ee2ca50 com.google.android.settings.intelligence/10118} BLOCKED
10-25 09:33:34.412  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.426  2758  4174 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 09:33:34.426  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 09:33:34.427  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 09:33:34.427  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.429  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.531  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.718  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 09:33:34.732  2758  4023 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 09:33:34.741  2758  4023 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 09:33:35.549  2758  4117 D GhDiag  : relay dns -> 274B ok
10-25 09:33:35.549  2758  4110 D GhDiag  : relay dns -> 178B ok
10-25 09:33:35.552  2758  4085 D GhDiag  : relay dns -> 269B ok
10-25 09:33:35.554  2758  4078 D GhDiag  : relay dns -> 173B ok
10-25 09:33:35.592  2758  4285 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:35.982  1417  3284 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 09:33:36.084  1468  3196 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 09:33:36.146  2758  4120 D GhDiag  : relay dns -> 45B ok
10-25 09:33:36.236  2758  4215 D GhDiag  : relay dns -> 260B ok
10-25 09:33:36.253  2758  4216 D GhDiag  : relay dns -> 164B ok
10-25 09:33:36.257  2758  4323 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.472   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{2716419 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 09:33:36.472   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{b1d6cde com.android.camera2/10145} BLOCKED
10-25 09:33:36.472   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{4672ebf com.google.android.gm/10147} BLOCKED
10-25 09:33:36.472   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{6e7498c com.google.android.devicelockcontroller/10170} BLOCKED
10-25 09:33:36.472   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{72b28d5 com.google.android.rkpdapp/10171} BLOCKED
10-25 09:33:36.472   519   570 I AppsFilter: interaction: PackageSetting{8c54071 com.ghprotocol.app/10192} -> PackageSetting{7624b7 com.google.android.projection.gearhead/10123} BLOCKED
10-25 09:33:36.508  2758  4232 D GhDiag  : relay dns -> 273B ok
10-25 09:33:36.514  2758  4231 D GhDiag  : relay dns -> 177B ok
10-25 09:33:36.693  2758  4338 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.694  2758  4126 D GhDiag  : relay dns -> 29B ok
10-25 09:33:36.737  2758  4340 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:36.984  2758  4348 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:37.208  2758  4293 D GhDiag  : relay dns -> 44B ok
10-25 09:33:37.225  2758  4292 D GhDiag  : relay dns -> 112B ok
10-25 09:33:37.752  1645  1645 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 09:33:37.909  1645  1645 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 09:33:37.928  1645  3831 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 09:33:37.928  1645  3831 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 09:33:38.912  2758  4392 D GhDiag  : relay dns -> 160B ok
10-25 09:33:38.921  2758  4393 D GhDiag  : relay dns -> 256B ok
10-25 09:33:38.926  2758  4562 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 09:33:39.245  2758  4565 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 09:33:39.318  2758  4570 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
10-25 09:33:39.370  2758  4339 D GhDiag  : relay dns -> 29B ok
10-25 09:33:39.392  2758  4576 D GhDiag  : relay tcp 5.61.x.x:443 -> socks5 ok
10-25 09:33:39.925  2758  4538 D GhDiag  : relay dns -> 160B ok
10-25 09:33:39.944  2758  4539 D GhDiag  : relay dns -> 256B ok

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
