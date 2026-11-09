import Reveal from "@/components/kit/Reveal";
import SavedList from "@/components/kit/SavedList";

export default function Home() {
  return (
    <main className="container">
      <div className="grid">
        <Reveal order={0} className="hero">
          <h1>Coming soon</h1>
          <p className="prose">This page is a placeholder until the crew writes the product.</p>
          <p>
            <a className="cta" href="#about">
              Learn more
            </a>
          </p>
        </Reveal>
        <Reveal order={1} className="panel">
          <section id="about" aria-labelledby="about-title">
            <h2 id="about-title">About</h2>
            <p className="prose">
              The crew replaces this section with the product. Notes saved here stay on this
              device.
            </p>
            <SavedList />
          </section>
        </Reveal>
      </div>
    </main>
  );
}
