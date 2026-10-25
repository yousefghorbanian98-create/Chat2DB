## gh-protocol E2E log — 2026-10-25T10:04:53Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T10:03:23Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 09:55 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 10:03 .
drwxr-xr-x 3 runner runner 4096 Oct 25 10:03 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 10:03 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 10:03 gh_test.ini

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
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2923
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
WARNING: cannnot unmap ptr 0x7fbf07c01000 as it is in the protected range from 0x7fbe07c00000 to 0x7fbf07e00000
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
INFO         | Boot completed in 32129 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
INFO         | Wait for emulator (pid 2923) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms

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
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:extractDeepLinksDebug
> Task :app:javaPreCompileDebug
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:packageDebugResources
> Task :app:mergeDebugAssets
> Task :app:processDebugMainManifest
> Task :app:compressDebugAssets
> Task :app:processDebugManifest
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugManifestForPackage
> Task :app:mergeDebugResources
> Task :app:parseDebugLocalResources
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugJniLibFolders
> Task :app:validateSigningDebug
> Task :app:mergeDebugNativeLibs
> Task :app:mergeLibDexDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

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
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792922441082.json

BUILD SUCCESSFUL in 2m 16s
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
app up (try 1, pid 3139)
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
    inet6 fe80::1cf1:2f4f:f339:5368/64 scope link stable-privacy 
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
10-25 10:04:39.810  3139  3139 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 10:04:39.810  3139  3139 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 10:04:40.165  3139  3139 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 10:04:40.213  3139  3139 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 10:04:40.331  3139  3139 D GhDiag  : connect: core.start=true 
10-25 10:04:45.866  3139  3139 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 10:04:45.999  3139  3139 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@685c385} — relay loop started
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=143
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=138
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=140
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=141
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=141
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=142
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=143
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.361  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.361  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.361  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:47.261  3139  4508 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 10:04:48.156  3139  4493 D GhDiag  : relay dns -> 274B ok
10-25 10:04:48.156  3139  4494 D GhDiag  : relay dns -> 178B ok
10-25 10:04:49.097  3139  4514 D GhDiag  : relay dns -> 260B ok
10-25 10:04:49.112  3139  4515 D GhDiag  : relay dns -> 164B ok
10-25 10:04:49.116  3139  4598 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:04:49.510  3139  4617 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:04:49.751  3139  4634 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:04:50.002  3139  4564 D GhDiag  : relay dns -> 44B ok
10-25 10:04:50.008  3139  4563 D GhDiag  : relay dns -> 112B ok
10-25 10:04:50.301  3139  4580 D GhDiag  : relay dns -> 152B ok
10-25 10:04:50.303  3139  4581 D GhDiag  : relay dns -> 88B ok
10-25 10:04:50.316  3139  4637 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 10:04:51.042  3139  4623 D GhDiag  : relay dns -> 45B ok
10-25 10:04:52.088  3139  4655 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 10:04:39.810  3139  3139 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 10:04:39.810  3139  3139 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 10:04:40.165  3139  3139 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 10:04:40.213  3139  3139 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 10:04:40.331  3139  3139 D GhDiag  : connect: core.start=true 
10-25 10:04:45.866  3139  3139 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 10:04:45.999  3139  3139 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@685c385} — relay loop started
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=143
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=138
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=140
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=141
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=141
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=142
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=143
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.361  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.361  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.361  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:47.261  3139  4508 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 10:04:48.156  3139  4493 D GhDiag  : relay dns -> 274B ok
10-25 10:04:48.156  3139  4494 D GhDiag  : relay dns -> 178B ok
10-25 10:04:49.097  3139  4514 D GhDiag  : relay dns -> 260B ok
10-25 10:04:49.112  3139  4515 D GhDiag  : relay dns -> 164B ok
10-25 10:04:49.116  3139  4598 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:04:49.510  3139  4617 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:04:49.751  3139  4634 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:04:50.002  3139  4564 D GhDiag  : relay dns -> 44B ok
10-25 10:04:50.008  3139  4563 D GhDiag  : relay dns -> 112B ok
10-25 10:04:50.301  3139  4580 D GhDiag  : relay dns -> 152B ok
10-25 10:04:50.303  3139  4581 D GhDiag  : relay dns -> 88B ok
10-25 10:04:50.316  3139  4637 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 10:04:51.042  3139  4623 D GhDiag  : relay dns -> 45B ok
10-25 10:04:52.088  3139  4655 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
10-25 10:04:52.275  3139  4625 D GhDiag  : relay dns -> 29B ok
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
esizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@76d184e} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{12f4d6f com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:04:31.382   523  2079 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 10:04:31.434   523  1948 D CoreBackPreview: Window{eb6d124 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@d6b9b9a, mPriority=0, mIsAnimationCallback=false}
10-25 10:04:31.864   523   540 V WindowManager: Sent Transition #6 createdAt=10-25 10:04:31.136 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=40197 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{eabf3e0 Task{eaa14a6 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{2c54699 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:04:31.864   523   540 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{eabf3e0 Task{eaa14a6 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0xa26b498 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{cd7dd5e Task{4340228 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0x5090f2 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:04:31.891   523   551 I ActivityManager: Start proc 3139:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 10:04:32.025  3139  3139 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 10:04:32.049  3139  3139 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 10:04:32.049  3139  3139 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 10:04:32.049  3139  3139 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 10:04:32.077   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{a1ee240 com.google.android.youtube/10139} BLOCKED
10-25 10:04:32.077   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{5960579 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 10:04:32.077   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{b2162be com.google.android.as/10124} BLOCKED
10-25 10:04:32.139   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{d9de221 com.google.android.gm/10140} BLOCKED
10-25 10:04:32.139   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{e87b007 com.google.android.devicelockcontroller/10179} BLOCKED
10-25 10:04:32.141   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{3d24534 com.google.android.dialer/10128} BLOCKED
10-25 10:04:32.142   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{bd57f5d com.google.android.contacts/10156} BLOCKED
10-25 10:04:32.142   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{5a3c0d2 com.google.android.partnersetup/10125} BLOCKED
10-25 10:04:32.148   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{fe545a3 com.google.android.apps.youtube.music/10155} BLOCKED
10-25 10:04:32.148   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{ee880a0 com.google.android.cellbroadcastreceiver/10172} BLOCKED
10-25 10:04:32.148   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{befb459 com.google.android.inputmethod.latin/10142} BLOCKED
10-25 10:04:32.534  3139  3139 W ziparchive: Unable to open '/data/app/~~gTFc55uoGIDy1T0k2qWB-Q==/com.ghprotocol.app-Wz9DoTOs4eVKHnLbSuBYSA==/base.dm': No such file or directory
10-25 10:04:32.534  3139  3139 W ziparchive: Unable to open '/data/app/~~gTFc55uoGIDy1T0k2qWB-Q==/com.ghprotocol.app-Wz9DoTOs4eVKHnLbSuBYSA==/base.dm': No such file or directory
10-25 10:04:32.782  3139  3139 D nativeloader: Configuring clns-6 for other apk /data/app/~~gTFc55uoGIDy1T0k2qWB-Q==/com.ghprotocol.app-Wz9DoTOs4eVKHnLbSuBYSA==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~gTFc55uoGIDy1T0k2qWB-Q==/com.ghprotocol.app-Wz9DoTOs4eVKHnLbSuBYSA==/lib/x86_64:/data/app/~~gTFc55uoGIDy1T0k2qWB-Q==/com.ghprotocol.app-Wz9DoTOs4eVKHnLbSuBYSA==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 10:04:32.825  3139  3139 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 10:04:32.825  3139  3139 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 10:04:33.367  3139  3139 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 10:04:33.367  3139  3139 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 10:04:33.367  3139  3139 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 10:04:33.372  3139  3139 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 10:04:33.372  3139  3139 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 10:04:33.373  3139  3139 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 10:04:33.373  3139  3139 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 10:04:33.492   523  2600 D CoreBackPreview: Window{d890eef u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@6aa6aa9, mPriority=0, mIsAnimationCallback=false}
10-25 10:04:34.483   523   540 W ziparchive: Unable to open '/data/app/~~gTFc55uoGIDy1T0k2qWB-Q==/com.ghprotocol.app-Wz9DoTOs4eVKHnLbSuBYSA==/base.dm': No such file or directory
10-25 10:04:34.485   523   540 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +3s402ms
10-25 10:04:34.525   523  2605 I ImeTracker: com.ghprotocol.app:3100a0c7: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 10:04:34.525   523  2605 I ImeTracker: com.ghprotocol.app:3100a0c7: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 10:04:34.555   523  2592 D CoreBackPreview: Window{eb6d124 u0 Splash Screen com.ghprotocol.app EXITING}: Setting back callback null
10-25 10:04:34.556   523  2592 W InputManager-JNI: Input channel object 'eb6d124 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 10:04:34.565  1494  1494 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 10:04:37.854   523  2605 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{b8178d3 com.google.android.gm/10140} BLOCKED
10-25 10:04:38.219  1558  1558 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 10:04:38.662  1558  1558 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 10:04:38.663  1558  2508 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 10:04:38.663  1558  2508 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 10:04:38.683  3139  3803 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 10:04:39.248   523   915 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{dad56c4 com.google.android.settings.intelligence/10118} BLOCKED
10-25 10:04:39.249   523   915 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{2d5d9ad com.google.android.settings.intelligence/10118} BLOCKED
10-25 10:04:39.523   523  2308 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 10:04:39.525   834   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@dbb5f97 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=48379 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@5b1e584} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{8c5216d com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:04:39.810  3139  3139 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 10:04:39.810  3139  3139 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 10:04:39.833  3905  3905 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 10:04:39.838  3905  3905 I AndroidRuntime: Using default boot image
10-25 10:04:39.838  3905  3905 I AndroidRuntime: Leaving lock profiling enabled
10-25 10:04:39.904  3951  3951 W libxraycore.so: type=1400 audit(0.0:15): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 10:04:39.908  3951  3951 W libxraycore.so: type=1400 audit(0.0:16): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 10:04:39.908  3951  3951 W libxraycore.so: type=1400 audit(0.0:17): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 10:04:39.908  3951  3951 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 10:04:40.100  3905  3905 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 10:04:40.165  3139  3139 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 10:04:40.213  3139  3139 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 10:04:40.331  3139  3139 D GhDiag  : connect: core.start=true 
10-25 10:04:40.392   523  2596 D CoreBackPreview: Window{d42e6d2 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@7fad863, mPriority=0, mIsAnimationCallback=false}
10-25 10:04:40.922   834   865 V WindowManagerShell: onTransitionReady android.os.BinderProxy@dbb5f97: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{ffc5a2f u0 com.ghprotocol.app/.MainActivity)/@0xea2b1fb sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{488ded0 u0 com.ghprotocol.app/.MainActivity)/@0xa27218 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:04:40.922   834   865 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{ffc5a2f u0 com.ghprotocol.app/.MainActivity)/@0xea2b1fb sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{488ded0 u0 com.ghprotocol.app/.MainActivity)/@0xa27218 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:04:40.922   523   540 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s419ms
10-25 10:04:40.922   523   540 V WindowManager: Sent Transition #7 createdAt=10-25 10:04:39.509 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=48379 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{eabf3e0 Task{eaa14a6 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{29ff408 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:04:40.922   523   540 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{ffc5a2f u0 com.ghprotocol.app/.MainActivity)/@0x2301bfa sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{488ded0 u0 com.ghprotocol.app/.MainActivity)/@0x6cb2e25 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:04:40.922   834   865 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{ffc5a2f u0 com.ghprotocol.app/.MainActivity)/@0xea2b1fb sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{488ded0 u0 com.ghprotocol.app/.MainActivity)/@0xa27218 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:04:41.240   834   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@a26de65 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=49800 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@16da73a} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{5800feb com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:04:41.248  3905  3905 D AndroidRuntime: Shutting down VM
10-25 10:04:41.352   523  2603 I ImeTracker: com.ghprotocol.app:9dc72bcd: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 10:04:41.352   523  2603 I ImeTracker: com.ghprotocol.app:9dc72bcd: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 10:04:41.357  1494  1494 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 10:04:41.611   523  2036 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 10:04:41.612   523  2036 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 10:04:41.612   523  2036 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 10:04:41.704  4025  4025 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=55719 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 10:04:42.483   523   540 V WindowManager: Sent Transition #8 createdAt=10-25 10:04:40.940 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=49800 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{eabf3e0 Task{eaa14a6 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{7f7350d com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:04:42.785  4151  4151 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 10:04:42.808  4151  4151 I AndroidRuntime: Using default boot image
10-25 10:04:42.808  4151  4151 I AndroidRuntime: Leaving lock profiling enabled
10-25 10:04:42.825   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{cfe0291 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 10:04:42.825   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{a1575f6 com.android.camera2/10148} BLOCKED
10-25 10:04:42.825   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{7585df7 com.google.android.gm/10140} BLOCKED
10-25 10:04:42.825   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{14b7464 com.google.android.devicelockcontroller/10179} BLOCKED
10-25 10:04:42.825   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{3ef36cd com.google.android.rkpdapp/10176} BLOCKED
10-25 10:04:42.825   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{f1afb82 com.google.android.contacts/10156} BLOCKED
10-25 10:04:42.825   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{faae293 com.google.android.settings.intelligence/10118} BLOCKED
10-25 10:04:42.825   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{3327369 com.google.android.projection.gearhead/10123} BLOCKED
10-25 10:04:42.825   523   574 I AppsFilter: interaction: PackageSetting{497a9c3 com.ghprotocol.app/10192} -> PackageSetting{d7d72d0 com.google.android.apps.youtube.music/10155} BLOCKED
10-25 10:04:42.953  4151  4151 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 10:04:43.218  3139  3157 I .ghprotocol.app: Background concurrent copying GC freed 99767(5249KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6500KB/12MB, paused 35us,8us total 1.117s
10-25 10:04:44.017  1437  4120 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 10:04:44.068  4151  4151 D AndroidRuntime: Shutting down VM
10-25 10:04:44.333  1403  3777 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 10:04:45.347   523  2353 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 10:04:45.859   523   536 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 10:04:45.866  3139  3139 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 10:04:45.997   523  1207 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 10:04:45.999  3139  3139 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@685c385} — relay loop started
10-25 10:04:46.069   523  1628 I ImeTracker: com.ghprotocol.app:7f8cf6e4: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 10:04:46.069   523  1628 I ImeTracker: com.ghprotocol.app:7f8cf6e4: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 10:04:46.078  1494  1494 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=143
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=138
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.359  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=139
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=140
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=141
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=141
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=142
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=143
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.360  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.361  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.361  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:46.361  3139  4464 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=144
10-25 10:04:47.261  3139  4508 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 10:04:48.156  3139  4493 D GhDiag  : relay dns -> 274B ok
10-25 10:04:48.156  3139  4494 D GhDiag  : relay dns -> 178B ok
10-25 10:04:49.097  3139  4514 D GhDiag  : relay dns -> 260B ok
10-25 10:04:49.112  3139  4515 D GhDiag  : relay dns -> 164B ok
10-25 10:04:49.116  3139  4598 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:04:49.510  3139  4617 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:04:49.751  3139  4634 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:04:50.002  3139  4564 D GhDiag  : relay dns -> 44B ok
10-25 10:04:50.008  3139  4563 D GhDiag  : relay dns -> 112B ok
10-25 10:04:50.301  3139  4580 D GhDiag  : relay dns -> 152B ok
10-25 10:04:50.303  3139  4581 D GhDiag  : relay dns -> 88B ok
10-25 10:04:50.316  3139  4637 D GhDiag  : relay tcp 142.251.x.x:443 -> socks5 ok
10-25 10:04:51.042  3139  4623 D GhDiag  : relay dns -> 45B ok
10-25 10:04:52.088  3139  4655 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
10-25 10:04:52.275  3139  4625 D GhDiag  : relay dns -> 29B ok

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
