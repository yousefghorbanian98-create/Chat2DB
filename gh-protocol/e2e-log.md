## gh-protocol E2E log — 2026-10-25T17:58:30Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T17:57:03Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 17:51 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 17:57 .
drwxr-xr-x 3 runner runner 4096 Oct 25 17:57 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 17:57 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 17:57 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2845
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
WARNING: cannnot unmap ptr 0x7fcf2ca01000 as it is in the protected range from 0x7fce2ca00000 to 0x7fcf2cc00000
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
INFO         | Boot completed in 31953 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 111
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 2845) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:37679 is gone due to Stream removed (CANCELLED)

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
> Task :app:mergeDebugAssets
> Task :app:parseDebugLocalResources
> Task :app:checkDebugDuplicateClasses
> Task :app:compressDebugAssets
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugResources
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:validateSigningDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:mergeLibDexDebug
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792950852473.json

BUILD SUCCESSFUL in 2m 25s
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
app up (try 1, pid 2861)
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
    inet6 fe80::dc50:fc8e:cdfe:d920/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.113.3): 56(84) bytes.

--- 140.82.113.3 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
--------- beginning of main
10-25 17:58:14.170  2861  2861 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 17:58:14.170  2861  2861 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 17:58:14.485  2861  2861 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 17:58:14.534  2861  2861 D GhDiag  : connect: config written bytes=5129 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 17:58:14.736  2861  2861 D GhDiag  : connect: core.start=true 
10-25 17:58:21.043  2861  2861 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 17:58:21.267  2861  2861 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@a163218} — relay loop started
10-25 17:58:21.419  2861  3005 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (45ms)
10-25 17:58:21.753  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:21.769  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 17:58:21.769  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 17:58:21.808  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=60
10-25 17:58:21.841  2861  4207 D GhDiag  : relay dns -> 178B ok
10-25 17:58:21.845  2861  4206 D GhDiag  : relay dns -> 274B ok
10-25 17:58:21.885  2861  4218 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:21.892  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:21.892  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=557
10-25 17:58:21.895  2861  4164 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 17:58:21.982  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:21.982  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:22.005  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 17:58:22.110  2861  4164 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 17:58:22.144  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.145  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.145  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.150  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=120
10-25 17:58:22.212  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=101
10-25 17:58:22.408  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:22.408  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.408  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 17:58:22.419  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 17:58:22.434  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=423
10-25 17:58:22.559  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=222
10-25 17:58:22.572  2861  4255 D GhDiag  : relay dns -> 164B ok
10-25 17:58:22.602  2861  4254 D GhDiag  : relay dns -> 260B ok
10-25 17:58:22.638  2861  4164 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 17:58:22.638  2861  4164 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 17:58:22.650  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.736  2861  4262 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:22.752  2861  4261 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 17:58:25.772  2861  4515 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:26.069  2861  4524 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 17:58:14.170  2861  2861 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 17:58:14.170  2861  2861 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 17:58:14.485  2861  2861 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 17:58:14.534  2861  2861 D GhDiag  : connect: config written bytes=5129 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 17:58:14.736  2861  2861 D GhDiag  : connect: core.start=true 
10-25 17:58:21.043  2861  2861 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 17:58:21.267  2861  2861 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@a163218} — relay loop started
10-25 17:58:21.419  2861  3005 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (45ms)
10-25 17:58:21.753  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:21.769  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 17:58:21.769  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 17:58:21.808  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=60
10-25 17:58:21.841  2861  4207 D GhDiag  : relay dns -> 178B ok
10-25 17:58:21.845  2861  4206 D GhDiag  : relay dns -> 274B ok
10-25 17:58:21.885  2861  4218 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:21.892  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:21.892  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=557
10-25 17:58:21.895  2861  4164 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 17:58:21.982  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:21.982  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:22.005  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 17:58:22.110  2861  4164 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 17:58:22.144  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.145  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.145  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.150  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=120
10-25 17:58:22.212  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=101
10-25 17:58:22.408  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:22.408  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.408  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 17:58:22.419  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 17:58:22.434  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=423
10-25 17:58:22.559  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=222
10-25 17:58:22.572  2861  4255 D GhDiag  : relay dns -> 164B ok
10-25 17:58:22.602  2861  4254 D GhDiag  : relay dns -> 260B ok
10-25 17:58:22.638  2861  4164 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 17:58:22.638  2861  4164 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 17:58:22.650  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.736  2861  4262 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:22.752  2861  4261 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 17:58:25.772  2861  4515 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:26.069  2861  4524 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:28.066  2861  4587 D GhDiag  : relay dns -> 160B ok
10-25 17:58:28.066  2861  4588 D GhDiag  : relay dns -> 256B ok
10-25 17:58:28.213  2861  4600 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)

10-25 17:57:40.079   336   336 I AndroidRuntime: Leaving lock profiling enabled
10-25 17:57:57.069   951   951 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-25 17:58:04.981   519   571 V BackupManagerService: [UserID:0] restoreAtInstall pkg=com.ghprotocol.app token=1 restoreSet=0
10-25 17:58:05.688   519  2620 V SplashScreenExceptionList: SplashScreen checking exception for package com.ghprotocol.app (target sdk:35) -> false
10-25 17:58:05.690   519  2620 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 17:58:05.796   519   901 D CoreBackPreview: Window{8aaefe3 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@35bc31a, mPriority=0, mIsAnimationCallback=false}
10-25 17:58:05.968   519   548 I ActivityManager: Start proc 2861:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 17:58:06.144  2861  2861 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 17:58:06.159  2861  2861 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 17:58:06.159  2861  2861 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 17:58:06.159  2861  2861 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 17:58:06.178   519   536 V WindowManager:     info={id=5 t=CLOSE f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{a67309a Task{5297867 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=MOVE_TO_TOP leash=Surface(name=Task=8)/@0x98ec589 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{fdacdcb Task{59ab0c3 #1 type=home}}} m=TO_BACK f=NONE leash=Surface(name=Task=1)/@0x9e325f0 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 17:58:06.439  2861  2861 W ziparchive: Unable to open '/data/app/~~LlFG7WQ9tF0KGSnaderdyQ==/com.ghprotocol.app-onTOj3JJAT93sJNSgQXPOw==/base.dm': No such file or directory
10-25 17:58:06.439  2861  2861 W ziparchive: Unable to open '/data/app/~~LlFG7WQ9tF0KGSnaderdyQ==/com.ghprotocol.app-onTOj3JJAT93sJNSgQXPOw==/base.dm': No such file or directory
10-25 17:58:06.888  2861  2861 D nativeloader: Configuring clns-6 for other apk /data/app/~~LlFG7WQ9tF0KGSnaderdyQ==/com.ghprotocol.app-onTOj3JJAT93sJNSgQXPOw==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~LlFG7WQ9tF0KGSnaderdyQ==/com.ghprotocol.app-onTOj3JJAT93sJNSgQXPOw==/lib/x86_64:/data/app/~~LlFG7WQ9tF0KGSnaderdyQ==/com.ghprotocol.app-onTOj3JJAT93sJNSgQXPOw==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 17:58:06.899  2861  2861 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 17:58:06.899  2861  2861 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 17:58:06.915   519   799 I SdkSandboxManager: No SDKs used. Skipping SDK data reconcilation for CallingInfo{mUid=10192, mPackageName='com.ghprotocol.app, mAppProcessToken='null'}
10-25 17:58:07.457  2861  2861 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 17:58:07.457  2861  2861 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 17:58:07.457  2861  2861 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 17:58:07.457  2861  2861 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 17:58:07.457  2861  2861 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 17:58:07.457  2861  2861 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 17:58:07.457  2861  2861 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 17:58:07.982   831   831 I SafetyLabelChangedBroadcastReceiver: received broadcast packageName: com.ghprotocol.app, current user: UserHandle{0}, packageChangeEvent: NEW_INSTALL, intent user: UserHandle{0}
10-25 17:58:07.987   519  2259 D CoreBackPreview: Window{77fc227 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@96e8a55, mPriority=0, mIsAnimationCallback=false}
10-25 17:58:09.251   519  2621 I WindowManager: finishDrawing of relaunch: Window{77fc227 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity} 2335ms
10-25 17:58:09.275   519   536 W ziparchive: Unable to open '/data/app/~~LlFG7WQ9tF0KGSnaderdyQ==/com.ghprotocol.app-onTOj3JJAT93sJNSgQXPOw==/base.dm': No such file or directory
10-25 17:58:09.279   519   536 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s600ms
10-25 17:58:09.309   519  2622 D CoreBackPreview: Window{8aaefe3 u0 Splash Screen com.ghprotocol.app}: Setting back callback null
10-25 17:58:09.316  1037  1037 D CarrierSvcBindHelper: onPackageAdded: com.ghprotocol.app
10-25 17:58:09.322   519   883 W InputManager-JNI: Input channel object '8aaefe3 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 17:58:10.212  1037  1286 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 17:58:10.213  1037  1037 D CarrierSvcBindHelper: onPackageModified: com.ghprotocol.app
10-25 17:58:10.227  1037  1286 D ImsResolver: maybeAddedImsService, packageName: com.ghprotocol.app
10-25 17:58:10.354   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{32e3ba6 com.google.android.youtube/10139} BLOCKED
10-25 17:58:10.354   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{94029e7 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 17:58:10.354   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{cc06994 com.google.android.as/10126} BLOCKED
10-25 17:58:10.354   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{a903c3d com.google.android.gm/10141} BLOCKED
10-25 17:58:10.354   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{5f26c32 com.google.android.devicelockcontroller/10190} BLOCKED
10-25 17:58:10.354   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{5db7d83 com.google.android.dialer/10128} BLOCKED
10-25 17:58:10.355   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{5048b00 com.google.android.contacts/10154} BLOCKED
10-25 17:58:10.355   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{7495f39 com.google.android.partnersetup/10124} BLOCKED
10-25 17:58:10.355   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{457197e com.google.android.apps.youtube.music/10156} BLOCKED
10-25 17:58:10.355   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{84e6edf com.google.android.cellbroadcastreceiver/10176} BLOCKED
10-25 17:58:10.355   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{ea7572c com.google.android.inputmethod.latin/10143} BLOCKED
10-25 17:58:10.796   519  2621 D CoreBackPreview: Window{77fc227 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback null
10-25 17:58:10.888   519  2196 W InputManager-JNI: Input channel object '77fc227 com.ghprotocol.app/com.ghprotocol.app.MainActivity (client)' was disposed without first being removed with the input manager!
10-25 17:58:11.167   519  2259 D CoreBackPreview: Window{a510a3 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@ce2b8bb, mPriority=0, mIsAnimationCallback=false}
10-25 17:58:11.713   519  1640 I ImeTracker: com.ghprotocol.app:7d2d8b43: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 17:58:11.713   519  1640 I ImeTracker: com.ghprotocol.app:7d2d8b43: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 17:58:11.716  1493  1493 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 17:58:12.369  1087  1132 I Launcher.IconCache: Database bulk icon loading failed, using fallback bulk icon loading for: ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 17:58:12.912  2861  3460 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 17:58:13.957   829   863 V WindowManagerShell: Transition requested: android.os.BinderProxy@9a54ce6 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=43697 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@8b40227} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{e76fcd4 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 17:58:13.957   519  2618 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 17:58:14.150  3648  3648 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 17:58:14.159  3648  3648 I AndroidRuntime: Using default boot image
10-25 17:58:14.163  3648  3648 I AndroidRuntime: Leaving lock profiling enabled
10-25 17:58:14.170  2861  2861 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 17:58:14.170  2861  2861 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 17:58:14.282  3664  3664 W libxraycore.so: type=1400 audit(0.0:15): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 17:58:14.290  3664  3664 W libxraycore.so: type=1400 audit(0.0:16): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 17:58:14.290  3664  3664 W libxraycore.so: type=1400 audit(0.0:17): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 17:58:14.290  3664  3664 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 17:58:14.416  3648  3648 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 17:58:14.485  2861  2861 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 17:58:14.534  2861  2861 D GhDiag  : connect: config written bytes=5129 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 17:58:14.736  2861  2861 D GhDiag  : connect: core.start=true 
10-25 17:58:15.210   519   587 D CoreBackPreview: Window{5f1afdc u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@22dd48d, mPriority=0, mIsAnimationCallback=false}
10-25 17:58:15.609  3648  3648 D AndroidRuntime: Shutting down VM
10-25 17:58:15.662  1601  1601 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 17:58:15.930   519   536 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s983ms
10-25 17:58:15.930   519   536 V WindowManager: Sent Transition #6 createdAt=10-25 17:58:13.942 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=43697 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{a67309a Task{5297867 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{d7a9eea com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 17:58:15.930   519   536 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{402dc5a u0 com.ghprotocol.app/.MainActivity)/@0xa587f8c sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{bc9b426 u0 com.ghprotocol.app/.MainActivity)/@0x2a37cbf sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 17:58:15.944   829   863 V WindowManagerShell: onTransitionReady android.os.BinderProxy@9a54ce6: {id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{402dc5a u0 com.ghprotocol.app/.MainActivity)/@0x526eafc sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{bc9b426 u0 com.ghprotocol.app/.MainActivity)/@0x8130585 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 17:58:15.944   829   863 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{402dc5a u0 com.ghprotocol.app/.MainActivity)/@0x526eafc sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{bc9b426 u0 com.ghprotocol.app/.MainActivity)/@0x8130585 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 17:58:15.944   829   863 V WindowManagerShell: start default transition animation, info = {id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{402dc5a u0 com.ghprotocol.app/.MainActivity)/@0x526eafc sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{bc9b426 u0 com.ghprotocol.app/.MainActivity)/@0x8130585 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 17:58:16.475   519   539 W ActivityTaskManager: Activity top resumed state loss timeout for ActivityRecord{402dc5a u0 com.ghprotocol.app/.MainActivity t8}
10-25 17:58:16.475   519   539 W ActivityTaskManager: Activity pause timeout for ActivityRecord{402dc5a u0 com.ghprotocol.app/.MainActivity t8}
10-25 17:58:16.761   829   863 V WindowManagerShell: Transition requested: android.os.BinderProxy@9dcad7e TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=45710 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@d4672df} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{5790b2c com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 17:58:16.853   519  2623 I ImeTracker: com.ghprotocol.app:5293cfd6: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 17:58:16.853   519  2623 I ImeTracker: com.ghprotocol.app:5293cfd6: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 17:58:16.865  1493  1493 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 17:58:17.127  2861  2913 W .ghprotocol.app: Cleared Reference was only reachable from finalizer (only reported once)
10-25 17:58:17.137  2861  2913 I .ghprotocol.app: Background concurrent copying GC freed 125370(6252KB) AllocSpace objects, 27(764KB) LOS objects, 49% free, 7234KB/14MB, paused 22us,8us total 682.730ms
10-25 17:58:17.180   519  2620 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{2e5470 com.google.android.gm/10141} BLOCKED
10-25 17:58:17.279  3948  3948 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 17:58:17.282  3948  3948 I AndroidRuntime: Using default boot image
10-25 17:58:17.282  3948  3948 I AndroidRuntime: Leaving lock profiling enabled
10-25 17:58:17.440  3948  3948 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 17:58:17.692   519  2116 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 17:58:17.697   519  2116 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 17:58:17.697   519  2116 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 17:58:18.354   519   536 V WindowManager: Sent Transition #7 createdAt=10-25 17:58:15.956 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=45710 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{a67309a Task{5297867 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{1cb32c8 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 17:58:18.457  1601  1601 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 17:58:18.458  1601  3476 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 17:58:18.458  1601  3476 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 17:58:19.359  1436  3047 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 17:58:19.710  3948  3948 D AndroidRuntime: Shutting down VM
10-25 17:58:20.111   519  2462 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{e2a846b com.google.android.settings.intelligence/10118} BLOCKED
10-25 17:58:20.112   519  2631 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{2352bc8 com.google.android.settings.intelligence/10118} BLOCKED
10-25 17:58:20.605  1386  3516 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 17:58:20.825   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{601de0d com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 17:58:20.825   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{b81b1c2 com.android.camera2/10147} BLOCKED
10-25 17:58:20.825   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{86dfbd3 com.google.android.devicelockcontroller/10190} BLOCKED
10-25 17:58:20.825   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{1c0b310 com.google.android.rkpdapp/10181} BLOCKED
10-25 17:58:20.835   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{7bd280e com.google.android.contacts/10154} BLOCKED
10-25 17:58:20.835   519   571 I AppsFilter: interaction: PackageSetting{d6c9101 com.ghprotocol.app/10192} -> PackageSetting{7124e3e com.google.android.projection.gearhead/10123} BLOCKED
10-25 17:58:20.898   519  2225 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 17:58:21.040   519  2225 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 17:58:21.043  2861  2861 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 17:58:21.264   519  2002 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 17:58:21.267  2861  2861 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@a163218} — relay loop started
10-25 17:58:21.419  2861  3005 D GhDiag  : relay tcp 1.1.x.x:80 -> socks5 ok (45ms)
10-25 17:58:21.743   519  1204 I ImeTracker: com.ghprotocol.app:d278965: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 17:58:21.743   519  1204 I ImeTracker: com.ghprotocol.app:d278965: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 17:58:21.752  1493  1493 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 17:58:21.753  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:21.769  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 17:58:21.769  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 17:58:21.808  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=60
10-25 17:58:21.841  2861  4207 D GhDiag  : relay dns -> 178B ok
10-25 17:58:21.845  2861  4206 D GhDiag  : relay dns -> 274B ok
10-25 17:58:21.885  2861  4218 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:21.892  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:21.892  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=557
10-25 17:58:21.895  2861  4164 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 17:58:21.982  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:21.982  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:22.005  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 17:58:22.110  2861  4164 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 17:58:22.144  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.145  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.145  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.150  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=120
10-25 17:58:22.212  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=101
10-25 17:58:22.408  2861  4164 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 17:58:22.408  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.408  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 17:58:22.419  2861  4164 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=64
10-25 17:58:22.434  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=423
10-25 17:58:22.559  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=222
10-25 17:58:22.572  2861  4255 D GhDiag  : relay dns -> 164B ok
10-25 17:58:22.575  2861  2913 I .ghprotocol.app: Background young concurrent copying GC freed 96631(6610KB) AllocSpace objects, 2(40KB) LOS objects, 45% free, 7845KB/14MB, paused 23us,9us total 108.148ms
10-25 17:58:22.602  2861  4254 D GhDiag  : relay dns -> 260B ok
10-25 17:58:22.638  2861  4164 D GhDiag  : tun pkt proto=6 dst=142.251.x.x len=40
10-25 17:58:22.638  2861  4164 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 17:58:22.650  2861  4164 D GhDiag  : tun pkt proto=6 dst=172.217.x.x len=40
10-25 17:58:22.736  2861  4262 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:22.752  2861  4261 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 17:58:23.899  2861  2913 I .ghprotocol.app: Background young concurrent copying GC freed 82737(6602KB) AllocSpace objects, 0(0B) LOS objects, 32% free, 9808KB/14MB, paused 34us,9us total 218.462ms
10-25 17:58:25.772  2861  4515 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:26.069  2861  4524 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 17:58:26.397  2861  2913 I .ghprotocol.app: Background young concurrent copying GC freed 75485(6467KB) AllocSpace objects, 0(0B) LOS objects, 39% free, 8753KB/14MB, paused 35us,37us total 269.174ms

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
